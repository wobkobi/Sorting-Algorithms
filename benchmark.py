"""
benchmark.py

This module implements the core logic for executing sorting benchmarks across multiple array sizes.
It handles:
  - Generating array sizes.
  - Reading and writing CSV files (using functions from csv_utils.py).
  - Running benchmark iterations in parallel.
  - Aggregating and updating overall statistics.
  - Generating markdown reports (per-size ranking tables and individual algorithm reports).

If an algorithm's CSV data for a given size does not contain the desired number of iterations,
the missing iterations are computed and appended. The CSV is then sorted alphabetically.
A helper ensures that new data is appended on a new line if the process stops and restarts.

The number of worker processes is determined dynamically based on the current time of day:
  - Between 12 AM and 9 AM: 75% of available CPU cores are used.
  - Otherwise: 50% of available CPU cores are used.
This worker count is re-evaluated for each array size, and a message is printed only if it changes.
"""

import csv
import os
import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

# Import sorting algorithms.
from algorithms import *

# Import helper functions from utils.
from utils import (
    compute_median,
    format_time,
    run_iteration,
    compute_average,
)

# Import CSV utilities.
from csv_utils import (
    get_csv_results_for_size,
    sort_csv_alphabetically,
)

# Import markdown report functions.
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    Produces two progressions:
      - A geometric progression for small sizes (from 3 to 100 over 15 steps).
      - An exponential progression (doubling) for larger sizes (starting at 100 up to 1 trillion).

    Returns:
        list: Sorted list of unique array sizes.
    """
    n_small = 15
    # Calculate small sizes using a geometric progression.
    small_sizes = [
        int(round(5 * ((200 / 3) ** (i / (n_small - 1))))) for i in range(n_small)
    ]
    large_sizes = []
    size = 100
    # Calculate large sizes by doubling until reaching 1 trillion.
    while size < 1e12:
        large_sizes.append(int(size))
        size *= 2
    large_sizes.append(int(1e12))
    return sorted(set(small_sizes + large_sizes))


def get_num_workers():
    """
    Determine the number of worker processes based on the current time of day.

    If the current time is between 11:30 PM and 9:30 AM, 75% of available CPU cores are used.
    Otherwise, 50% of available CPU cores are used.

    Returns:
        int: The number of worker processes to use (at least 1).
    """
    total = os.cpu_count() or 1
    now = datetime.datetime.now().time()
    if datetime.time(23, 30) <= now or now <= datetime.time(9, 30):
        workers = max(int(total * 0.75), 1)
    else:
        workers = max(int(total * 0.5), 1)
    return workers


def algorithms():
    """
    Provide a dictionary mapping algorithm names to their sorting functions.

    Returns:
        dict: Mapping {algorithm_name: sorting_function, ...}
    """
    return {
        "Bead Sort": bead_sort,
        "Bitonic Sort Parallel": bitonic_sort_parallel,
        "Block Sort": block_sort,
        "Bogo Sort": bogo_sort,
        "Bubble Sort": bubble_sort,
        "Bucket Sort": bucket_sort,
        "Burst Sort": burst_sort,
        "Cocktail Sort": cocktail_sort,
        "Comb Sort": comb_sort,
        "Cycle Sort": cycle_sort,
        "Exchange Sort": exchange_sort,
        "External Merge Sort": external_merge_sort,
        "Flash Sort": flash_sort,
        "Franceschini's Method": franceschinis_method,
        "Gnome Sort": gnome_sort,
        "Heap Sort": heap_sort,
        "Hyper Quick": hyper_quick,
        "I Can't Believe It Can Sort": i_cant_believe_it_can_sort,
        "Insertion Sort": insertion_sort,
        "Intro Sort": intro_sort,
        "Library Sort": library_sort,
        "Merge Insertion Sort": merge_insertion_sort,
        "Merge Sort": merge_sort,
        "MSD Radix Sort": msd_radix_sort,
        "MSD Radix Sort In-Place": msd_radix_sort_inplace,
        "Odd-Even Sort": odd_even_sort,
        "P-Merge Sort": p_merge_sort,
        "Pancake Sort": pancake_sort,
        "Patience Sort": patience_sort,
        "Pigeonhole Sort": pigeonhole_sort,
        "Polyphase Merge Sort": polyphase_merge_sort,
        "Postman Sort": postman_sort,
        "Quick Sort": quick_sort,
        "Radix Sort": radix_sort,
        "Replacement Selection Sort": replacement_selection_sort,
        "Sample Sort": sample_sort,
        "Selection Sort": selection_sort,
        "Shell Sort": shell_sort,
        "Sleep Sort": sleep_sort,
        "Slowsort": slowsort,
        "Smooth Sort": smooth_sort,
        "Sorting Network": sorting_network,
        "Spaghetti Sort": spaghetti_sort,
        "Spreadsort": spreadsort,
        "Stooge Sort": stooge_sort,
        "Strand Sort": strand_sort,
        "Tim Sort": tim_sort,
        "Tournament Sort": tournament_sort,
        "Tree Sort": tree_sort,
    }


def update_missing_iterations(
    csv_path,
    size,
    expected_algs,
    size_results,
    iterations,
    skip_list,
    threshold,
    num_workers,
):
    """
    Identify and run additional iterations for algorithms with missing data.

    For each algorithm in expected_algs (not in skip_list) that has fewer than the desired
    number of iterations, determine how many are missing, print a consolidated message, run
    the additional iterations, and append the results to the CSV file.

    Parameters:
        csv_path (str): Path to the CSV file.
        size (int): Current array size.
        expected_algs (list): List of expected algorithm names.
        size_results (OrderedDict): Existing results for this size.
        iterations (int): Desired number of iterations per algorithm.
        skip_list (set): Set of algorithms to skip.
        threshold (int): Runtime threshold (in seconds) to determine if an algorithm should be skipped.
        num_workers (int): Number of worker processes to use.

    Returns:
        tuple: (updated size_results, updated skip_list)
    """
    missing_algs = {}
    found_msgs = []
    for alg in expected_algs:
        if alg in skip_list:
            continue
        data = size_results[alg]
        if data is None:
            missing_algs[alg] = iterations
        else:
            count = data[4]  # Number of iterations recorded.
            if count < iterations:
                missing_algs[alg] = iterations - count
                found_msgs.append(f"{alg} ({count})")
    if missing_algs:
        if found_msgs:
            # Display only half of the found messages (at least one).
            max_items = max(1, len(found_msgs) // 2)
            if len(found_msgs) > max_items:
                display_msg = (
                    ", ".join(found_msgs[:max_items])
                    + f", and {len(found_msgs) - max_items} others"
                )
            else:
                display_msg = ", ".join(found_msgs)
            print(
                f"Found existing results for: {display_msg}; running additional iterations."
            )
        else:
            print(f"Missing iterations for: {', '.join(missing_algs.keys())}")
        # Run additional iterations for each algorithm with missing data.
        with open(csv_path, "a", newline="") as csv_file:
            writer = csv.writer(csv_file)
            for alg_name, additional in missing_algs.items():
                sort_func = algorithms()[alg_name]
                new_times = []
                with ProcessPoolExecutor(max_workers=num_workers) as executor:
                    futures = [
                        executor.submit(run_iteration, sort_func, size)
                        for _ in range(additional)
                    ]
                    start_iter = (
                        size_results[alg_name][4] + 1
                        if size_results[alg_name] is not None
                        else 1
                    )
                    for i, future in enumerate(as_completed(futures), start=start_iter):
                        try:
                            t = future.result()
                            new_times.append(t)
                            writer.writerow([alg_name, size, i, f"{t:.8f}"])
                            csv_file.flush()
                        except Exception as e:
                            print(f"{alg_name} error on size {size} iteration {i}: {e}")
                            new_times = []
                            break
                if new_times:
                    combined = (
                        new_times
                        if size_results[alg_name] is None
                        else size_results[alg_name][5] + new_times
                    )
                    avg = compute_average(combined)
                    median = compute_median(combined)
                    size_results[alg_name] = (
                        avg,
                        min(combined),
                        max(combined),
                        median,
                        len(combined),
                        combined,
                    )
                    print(f"Average for {alg_name} on size {size}: {format_time(avg)}")
                    if avg > threshold and alg_name not in skip_list:
                        skip_list.add(alg_name)
                        print(f"Skipping {alg_name} for future sizes (average > 5min).")
                else:
                    size_results[alg_name] = None
    return size_results, skip_list


def update_overall_results(
    size, size_results, expected_algs, overall_totals, per_alg_results, iterations
):
    """
    Update the aggregated overall totals and per-algorithm results for a given array size.

    Parameters:
        size (int): The current array size.
        size_results (OrderedDict): Benchmark results for this size.
        expected_algs (list): List of expected algorithm names.
        overall_totals (dict): Aggregated totals, updated in place.
        per_alg_results (dict): Per-algorithm results list, updated in place.
        iterations (int): The desired number of iterations per algorithm.
    """
    for alg in expected_algs:
        data = size_results[alg]
        if data is not None:
            overall_totals[alg]["sum"] += data[0] * iterations
            overall_totals[alg]["count"] += iterations
            per_alg_results[alg].append((size, data[0], data[1], data[2], data[3]))


def process_size(
    size,
    iterations,
    threshold,
    expected_algs,
    overall_totals,
    per_alg_results,
    skip_list,
):
    """
    Process a single array size by updating CSV results, running missing iterations,
    and updating aggregated statistics.

    Parameters:
        size (int): The current array size.
        iterations (int): Desired iterations per algorithm.
        threshold (int): Threshold in seconds to decide if an algorithm should be skipped.
        expected_algs (list): List of expected algorithm names.
        overall_totals (dict): Aggregated totals (to be updated).
        per_alg_results (dict): Per-algorithm results (to be updated).
        skip_list (set): Set of algorithms to be skipped (to be updated).

    Returns:
        tuple: (updated size_results, updated skip_list)
    """
    csv_path, size_results = get_csv_results_for_size(size, expected_algs)
    # Re-evaluate worker count for this array size.
    current_workers = get_num_workers()
    # (Print worker count message only if changed.)
    process_size.workers = getattr(process_size, "workers", None)
    if process_size.workers is None or current_workers != process_size.workers:
        if process_size.workers is None:
            print(
                f"Using {current_workers} worker{'s' if current_workers > 1 else ''} for array size {size}."
            )
        else:
            print(
                f"Changing workers from {process_size.workers} to {current_workers} for array size {size}."
            )
        process_size.workers = current_workers

    size_results, skip_list = update_missing_iterations(
        csv_path,
        size,
        expected_algs,
        size_results,
        iterations,
        skip_list,
        threshold,
        current_workers,
    )
    # Sort the CSV file alphabetically.
    sort_csv_alphabetically(csv_path)
    update_overall_results(
        size, size_results, expected_algs, overall_totals, per_alg_results, iterations
    )
    return size_results, skip_list


def run_sorting_tests(iterations=250, threshold=300):
    """
    Execute sorting benchmarks across various array sizes and compile the results.

    Parameters:
        iterations (int): Number of iterations per algorithm per array size (default: 250).
        threshold (int): Threshold in seconds for average runtime; algorithms exceeding this are skipped (default: 300).

    The process for each array size:
      1. Retrieve or create the CSV file and read its current contents.
      2. Re-evaluate the number of worker processes for the current size.
      3. Identify algorithms with missing iterations and run additional iterations to fill the gap.
      4. Ensure the CSV ends with a newline, then sort it alphabetically.
      5. Update aggregated overall totals and per-algorithm results.
      6. Append a per-size markdown ranking table (with notes for any skipped algorithms) to a details file.
      7. Rebuild the main README.md file to display overall top-20 rankings and the list of skipped algorithms.

    Algorithms with an average runtime exceeding the threshold are skipped in future sizes.
    """
    sizes = generate_sizes()
    expected_algs = list(algorithms().keys())
    overall_totals = {alg: {"sum": 0, "count": 0} for alg in expected_algs}
    per_alg_results = {alg: [] for alg in expected_algs}
    skip_list = set()

    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)

    details_path = "details.md"
    with open(details_path, "w") as f:
        f.write("")

    # Process each array size.
    for size in sizes:
        print(f"\nTesting array size: {size}")
        size_results, skip_list = process_size(
            size,
            iterations,
            threshold,
            expected_algs,
            overall_totals,
            per_alg_results,
            skip_list,
        )
        # Determine newly skipped algorithms for this size.
        previous_skip = set(skip_list)
        for alg, data in size_results.items():
            if data is not None and data[0] > threshold:
                skip_list.add(alg)
        new_skipped = skip_list - previous_skip
        # Append per-size markdown ranking table.
        with open(details_path, "a") as f:
            write_markdown(f, size, size_results, removed=list(new_skipped))
        # Rebuild the main README.
        rebuild_readme(overall_totals, details_path, skip_list)

    # Generate individual markdown files for each algorithm.
    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

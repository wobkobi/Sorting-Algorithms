"""
benchmark.py

This module implements the core logic for executing sorting benchmarks across multiple array sizes.
It handles:
  - Generating array sizes.
  - Reading and writing CSV files (using functions from csv_utils.py).
  - Running benchmark iterations concurrently across all algorithms.
  - Aggregating and updating overall statistics.
  - Generating markdown reports (per-size ranking tables and individual algorithm reports).

If an algorithm's CSV data for a given size does not contain the desired number of iterations,
the missing iterations are computed and appended concurrently. The CSV is then sorted alphabetically.
A helper ensures that new data is appended on a new line if the process stops and later restarts.

The number of worker processes is determined dynamically based on the current time of day:
  - Between 11:30 PM and 9:30 AM: 75% of available CPU cores are used.
  - Otherwise: 50% of available CPU cores are used.
If the SLOW_MODE environment variable is set to "true", the worker count is halved.
The worker count is re-evaluated for each array size and printed only if it changes.
"""

import csv
import os
import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

# Import sorting algorithms.
from algorithms import *

# Import helper functions from utils.
from utils import compute_median, format_time, run_iteration, compute_average


# Import CSV utility functions from csv_utils.py.
from csv_utils import get_csv_results_for_size, sort_csv_alphabetically

# Import markdown report functions.
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    This function creates two progressions:
      - A geometric progression for small sizes (from 3 to 100 over 15 steps).
      - An exponential progression (by doubling) for larger sizes (starting at 100 up to 1 trillion).

    Returns:
        list: A sorted list of unique array sizes.
    """
    n_small = 15
    # Calculate small sizes using a geometric progression.
    small_sizes = [
        int(round(5 * ((200 / 3) ** (i / (n_small - 1))))) for i in range(n_small)
    ]
    large_sizes = []
    size = 100
    # Double the size until reaching 1 trillion.
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
    Additionally, if the SLOW_MODE environment variable is set to "true", the worker count is halved.

    Returns:
        int: The number of worker processes to use (at least 1).
    """
    total = os.cpu_count() or 1
    now = datetime.datetime.now().time()
    # Determine worker ratio based on the time of day.
    if datetime.time(23, 30) <= now or now <= datetime.time(9, 30):
        workers = max(int(total * 0.75), 1)
    else:
        workers = max(int(total * 0.5), 1)
    # If slow mode is enabled, use half the number of workers.
    if os.environ.get("SLOW_MODE", "").lower() == "true":
        workers = max(int(workers * 0.5), 1)
    return workers


def algorithms():
    """
    Provide a dictionary mapping algorithm names to their corresponding sorting functions.

    Returns:
        dict: A dictionary mapping each algorithm's name (str) to its sorting function.
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


def update_missing_iterations_concurrent(
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
    Identify missing iterations for each algorithm and run them concurrently across all algorithms.

    For each algorithm (not in skip_list) with fewer than the desired iterations, determine the number
    of missing iterations. Then, submit a task for each missing iteration concurrently using a global pool.
    As each future completes, its result is immediately written to the CSV file and accumulated in the results.

    Parameters:
        csv_path (str): Path to the CSV file.
        size (int): The current array size.
        expected_algs (list): List of expected algorithm names.
        size_results (OrderedDict): Existing results for this size.
        iterations (int): Desired iterations per algorithm.
        skip_list (dict): Dictionary mapping algorithm names to the size at which they were skipped.
        threshold (int): Runtime threshold (in seconds) to decide if an algorithm should be skipped.
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
            count = data[4]  # Number of iterations already recorded.
            if count < iterations:
                missing_algs[alg] = iterations - count
                found_msgs.append(f"{alg} ({count})")
    # Print a consolidated message for debugging.
    if missing_algs:
        if found_msgs:
            max_items = min(len(found_msgs) // 2, 10)
            if len(found_msgs) == len(expected_algs) - len(missing_algs):
                display_msg = "all algorithms"
            elif len(found_msgs) > max_items:
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
        # Run missing iterations concurrently.
        with ProcessPoolExecutor(max_workers=num_workers) as executor:
            tasks = {}
            for alg, missing in missing_algs.items():
                start_iter = (
                    size_results[alg][4] + 1 if size_results[alg] is not None else 1
                )
                for i in range(missing):
                    future = executor.submit(run_iteration, algorithms()[alg], size)
                    tasks[future] = (alg, start_iter + i)
            with open(csv_path, "a", newline="") as csv_file:
                writer = csv.writer(csv_file)
                for future in as_completed(tasks):
                    alg, iter_index = tasks[future]
                    try:
                        t = future.result()
                        writer.writerow([alg, size, iter_index, f"{t:.8f}"])
                        csv_file.flush()
                        if size_results[alg] is None:
                            size_results[alg] = (None, None, None, None, 0, [])
                        # Update the count and append the new time.
                        size_results[alg] = (
                            None,  # avg (to be recalculated)
                            None,  # min (to be recalculated)
                            None,  # max (to be recalculated)
                            None,  # median (to be recalculated)
                            size_results[alg][4] + 1,
                            size_results[alg][5] + [t],
                        )
                    except Exception as e:
                        print(f"{alg} error on size {size} iteration {iter_index}: {e}")
        # Recalculate statistics for each algorithm with new data.
        for alg in missing_algs.keys():
            times = size_results[alg][5]
            avg = compute_average(times)
            median = compute_median(times)
            size_results[alg] = (avg, min(times), max(times), median, len(times), times)
            print(f"Average for {alg} on size {size}: {format_time(avg, False)}")
            if avg > threshold and alg not in skip_list:
                skip_list[alg] = size
                print(
                    f"Skipping {alg} for future sizes (average > 5min, skipped at size {size})."
                )
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
        overall_totals (dict): Aggregated totals (updated in place).
        per_alg_results (dict): Per-algorithm results (updated in place).
        iterations (int): Desired iterations per algorithm.
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
    Process a single array size:
      - Retrieve or create CSV results.
      - Re-evaluate the number of worker processes for the current size and print a message if it changes.
      - Update missing iterations concurrently across all algorithms.
      - Sort the CSV file and update aggregated overall statistics.

    Parameters:
        size (int): The current array size.
        iterations (int): Desired iterations per algorithm.
        threshold (int): Runtime threshold (in seconds).
        expected_algs (list): List of expected algorithm names.
        overall_totals (dict): Aggregated overall totals (updated in place).
        per_alg_results (dict): Per-algorithm results (updated in place).
        skip_list (dict): Dictionary mapping algorithms to the size at which they were skipped (updated in place).

    Returns:
        tuple: (updated size_results, updated skip_list)
    """
    csv_path, size_results = get_csv_results_for_size(size, expected_algs)
    # Re-evaluate the worker count for this size.
    current_workers = get_num_workers()
    process_size.workers = getattr(process_size, "workers", None)
    if process_size.workers is None or current_workers != process_size.workers:
        if process_size.workers is None:
            print(
                f"Using {current_workers} worker{'s' if current_workers > 1 else ''}."
            )
        else:
            print(
                f"Changing workers from {process_size.workers} worker{'s' if process_size.workers > 1 else ''} to {current_workers} worker{'s' if current_workers > 1 else ''}."
            )
        process_size.workers = current_workers

    # Update missing iterations concurrently.
    size_results, skip_list = update_missing_iterations_concurrent(
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
    # Update aggregated overall statistics.
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

    For each array size:
      1. Retrieve or create the CSV file and read its current contents.
      2. Re-evaluate the number of worker processes for the current size.
      3. Identify algorithms with missing iterations and run additional iterations concurrently.
      4. Ensure the CSV ends with a newline, then sort it alphabetically.
      5. Update aggregated overall totals and per-algorithm records.
      6. Append a per-size markdown ranking table (with notes for any newly skipped algorithms) to a details file.
      7. Rebuild the main README.md file with overall top-20 rankings and the list of skipped algorithms.

    Algorithms with an average runtime exceeding the threshold are skipped in future sizes.
    """
    sizes = generate_sizes()
    expected_algs = list(algorithms().keys())

    overall_totals = {alg: {"sum": 0, "count": 0} for alg in expected_algs}
    per_alg_results = {alg: [] for alg in expected_algs}
    skip_list = {}

    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)

    details_path = "details.md"
    with open(details_path, "w") as f:
        f.write("")

    # Determine and print the initial worker count before processing any sizes.
    initial_workers = get_num_workers()
    print(f"Using {initial_workers} worker{'s' if initial_workers > 1 else ''}.")
    process_size.workers = initial_workers

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
        previous_skip = set(skip_list.keys())
        for alg, data in size_results.items():
            if data is not None and data[0] > threshold and alg not in skip_list:
                skip_list[alg] = size
        new_skipped = {
            alg: skip_list[alg] for alg in skip_list if alg not in previous_skip
        }

        # Append per-size markdown ranking table with notes for any newly skipped algorithms.
        with open(details_path, "a") as f:
            write_markdown(f, size, size_results, removed=list(new_skipped.keys()))

        # Rebuild the main README with updated overall totals and skip list.
        rebuild_readme(overall_totals, details_path, skip_list)

    # Generate individual markdown files for each algorithm.
    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

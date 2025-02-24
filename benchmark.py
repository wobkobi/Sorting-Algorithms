"""
benchmark.py

This module implements the core logic for executing sorting benchmarks across multiple array sizes.
It performs the following tasks:
  - Generates a list of array sizes for benchmarking.
  - Reads and writes CSV files using functions from csv_utils.py.
  - Executes benchmark iterations in parallel.
  - Aggregates and updates overall statistics.
  - Generates markdown reports (both per-size ranking tables and individual algorithm reports).

If a CSV file for a given array size does not have the desired number of iterations,
the missing iterations are executed and appended to the CSV.
The CSV file is then sorted alphabetically.
A helper function ensures that new data is appended on a new line if the process stops and later resumes.
The number of worker processes is dynamically determined based on the current time of day:
  - Between 12 AM and 9 AM: 75% of available CPU cores are used.
  - Otherwise: 50% of available CPU cores are used.
The worker count is re-evaluated for each array size and only printed if it changes.
"""

import csv
import os
import time
import datetime
from collections import OrderedDict
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

# Import CSV utility functions from csv_utils.py.
from csv_utils import (
    read_csv_results,
    ensure_csv_ends_with_newline,
    sort_csv_alphabetically,
)

# Import markdown report functions.
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    This function produces two distinct progressions:
      - A geometric progression for small sizes (from 3 to 100, distributed over 15 steps).
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
    # Doubling for large sizes until 1e12.
    while size < 1e12:
        large_sizes.append(int(size))
        size *= 2
    large_sizes.append(int(1e12))
    return sorted(set(small_sizes + large_sizes))


def get_num_workers():
    """
    Determine the number of worker processes based on the current time of day.

    Uses:
      - 75% of available CPU cores if the time is between 12 AM and 9 AM.
      - 50% of available CPU cores otherwise.

    Returns:
        int: The number of worker processes to use (at least 1).
    """
    total = os.cpu_count() or 1
    now = datetime.datetime.now().time()
    if now.hour < 9:
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


def run_sorting_tests(iterations=250, threshold=300):
    """
    Execute sorting benchmarks across multiple array sizes and compile the results.

    Parameters:
        iterations (int): Number of iterations per algorithm per array size (default: 250).
        threshold (int): Time threshold (in seconds); algorithms exceeding this average are skipped (default: 300).

    Process for each array size:
      1. Check for an existing CSV file. If it exists, read its data using read_csv_results.
         Otherwise, create a new CSV file with the proper header.
      2. Ensure the CSV file ends with a newline (to prevent appending on the same line).
      3. Re-evaluate the number of worker processes via get_num_workers() for the current size.
         Print the worker count only if it changes from the previous array size.
      4. Identify algorithms that do not have the required number of iterations.
         A consolidated message is printed (showing half the items, with a summary of the remainder).
      5. For each algorithm with missing iterations, run the additional iterations in parallel
         and append the new data to the CSV.
      6. Sort the CSV alphabetically by algorithm name.
      7. Update overall aggregated statistics and per-algorithm results.
      8. Append a per-size markdown ranking table (with notes for any algorithms removed) to a details file.
      9. Rebuild the main README.md with overall top-20 rankings and the list of skipped algorithms.

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

    prev_workers = (
        None  # Track previous worker count to print message only if it changes.
    )

    # Process each array size.
    for size in sizes:
        print(f"\nTesting array size: {size}")
        csv_filename = f"results_{size}.csv"
        csv_path = os.path.join(output_folder, csv_filename)

        csv_exists = os.path.exists(csv_path)
        if csv_exists:
            print(f"CSV file for size {size} exists; reading results.")
            size_results = read_csv_results(csv_path, expected_algs)
        else:
            # Create new CSV file and write the header.
            with open(csv_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(
                    ["Algorithm", "Array Size", "Iteration", "Elapsed Time (seconds)"]
                )
            size_results = OrderedDict((alg, None) for alg in expected_algs)

        # Ensure the CSV ends with a newline.
        ensure_csv_ends_with_newline(csv_path)

        # Re-evaluate worker count for the current size.
        current_workers = get_num_workers()
        if prev_workers is None or current_workers != prev_workers:
            if prev_workers is None:
                print(
                    f"Using {current_workers} worker{'s' if current_workers > 1 else ''} for array size {size}."
                )
            else:
                print(
                    f"Changing workers from {prev_workers} to {current_workers} for array size {size}."
                )
            prev_workers = current_workers

        # Identify missing iterations for each algorithm.
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
        if csv_exists and missing_algs:
            if found_msgs:
                # Determine how many items to show: half of the found items (at least one).
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

        # Run additional iterations for algorithms with missing data.
        if missing_algs:
            with open(csv_path, "a", newline="") as csv_file:
                writer = csv.writer(csv_file)
                for alg_name, additional in missing_algs.items():
                    sort_func = algorithms()[alg_name]
                    new_times = []
                    with ProcessPoolExecutor(max_workers=current_workers) as executor:
                        futures = [
                            executor.submit(run_iteration, sort_func, size)
                            for _ in range(additional)
                        ]
                        # Determine starting iteration number.
                        start_iter = (
                            size_results[alg_name][4] + 1
                            if size_results[alg_name] is not None
                            else 1
                        )
                        for i, future in enumerate(
                            as_completed(futures), start=start_iter
                        ):
                            try:
                                t = future.result()
                                new_times.append(t)
                                writer.writerow([alg_name, size, i, f"{t:.8f}"])
                                csv_file.flush()
                            except Exception as e:
                                print(
                                    f"{alg_name} error on size {size} iteration {i}: {e}"
                                )
                                new_times = []
                                break
                    if new_times:
                        # Combine new times with any existing ones.
                        if size_results[alg_name] is None:
                            combined = new_times
                        else:
                            combined = size_results[alg_name][5] + new_times
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
                        print(
                            f"Average for {alg_name} on size {size}: {format_time(avg)}"
                        )
                        if avg > threshold and alg_name not in skip_list:
                            skip_list.add(alg_name)
                            print(
                                f"Skipping {alg_name} for future sizes (average > 5min)."
                            )
                    else:
                        size_results[alg_name] = None
            print(f"Updated CSV for size {size}.")

        # Sort the CSV alphabetically by algorithm name.
        sort_csv_alphabetically(csv_path)

        # Update overall totals and per-algorithm results.
        for alg in expected_algs:
            data = size_results[alg]
            if data is not None:
                overall_totals[alg]["sum"] += data[0] * iterations
                overall_totals[alg]["count"] += iterations
                per_alg_results[alg].append((size, data[0], data[1], data[2], data[3]))

        # Determine newly skipped algorithms for this size.
        previous_skip = set(skip_list)
        for alg, data in size_results.items():
            if data is not None and data[0] > threshold:
                skip_list.add(alg)
        new_skipped = skip_list - previous_skip

        # Append the per-size markdown ranking table with a note for removed algorithms.
        with open(details_path, "a") as f:
            write_markdown(f, size, size_results, removed=list(new_skipped))

        # Rebuild the main README with updated overall totals and skip list.
        rebuild_readme(overall_totals, details_path, skip_list)

    # Generate individual markdown files for each algorithm.
    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

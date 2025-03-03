"""
This module contains the core functions for running sorting algorithm benchmarks.
It handles:
  - Generating the array sizes to be tested.
  - Determining the number of worker processes.
  - Processing a given array size by scheduling missing iterations,
    updating the CSV file, and computing overall statistics.
  - Orchestrating the overall benchmark tests and generating reports.
"""

import os
import datetime
from algorithms import *  # Your sorting algorithms.
from algorithms_map import get_algorithms
from csv_utils import get_csv_results_for_size, sort_csv_alphabetically
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown
from benchmark_scheduler import update_missing_iterations_concurrent


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    This function uses two progressions:
      - A geometric progression for small array sizes.
      - An exponential (doubling) progression for large array sizes.
    The resulting sizes cover a wide range up to 1 trillion.

    Returns:
        List[int]: A sorted list of unique array sizes.
    """
    n_small = 15
    # Calculate small sizes using a geometric progression.
    small_sizes = [
        int(round(5 * ((200 / 3) ** (i / (n_small - 1))))) for i in range(n_small)
    ]
    large_sizes = []
    size = 100
    # Generate large sizes by doubling until reaching 1e12.
    while size < 1e12:
        large_sizes.append(int(size))
        size *= 2
    large_sizes.append(int(1e12))
    # Return the union of small and large sizes.
    return sorted(set(small_sizes + large_sizes))


def get_num_workers():
    """
    Determine the number of worker processes based on the current time and environment.

    The logic is as follows:
      - At night (between 11:30 PM and 9:30 AM), use 75% of available CPU cores.
      - During the day, use 50% of available CPU cores.
      - If the SLOW_MODE environment variable is set to "true", the number is halved.

    Returns:
        int: The number of worker processes (minimum of 1).
    """
    total = os.cpu_count() or 1
    now = datetime.datetime.now().time()
    # Use more cores at night and fewer during the day.
    if datetime.time(23, 30) <= now or now <= datetime.time(9, 30):
        workers = max(int(total * 0.75), 1)
    else:
        workers = max(int(total * 0.5), 1)
    # Halve the number if SLOW_MODE is enabled.
    if os.environ.get("SLOW_MODE", "").lower() == "true":
        workers = max(int(workers * 0.5), 1)
    return workers


def update_overall_results(
    size, size_results, expected_algs, overall_totals, per_alg_results, iterations
):
    """
    Update aggregated benchmark statistics with results from a given array size.

    For each algorithm, this function updates the overall sum and count (used to compute overall averages)
    and appends a performance record (size, average, min, max, median) to per_alg_results.

    Parameters:
        size (int): The current array size.
        size_results (dict): The computed statistics for each algorithm at this size.
        expected_algs (list): List of algorithm names.
        overall_totals (dict): Aggregated totals for each algorithm (keys: "sum" and "count").
        per_alg_results (dict): Per-algorithm performance records.
        iterations (int): Total iterations per algorithm.
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
    per_run_timeout=False,
):
    """
    Process benchmark tests for a single array size.

    This function:
      1. Retrieves (or creates) the CSV file for the given size.
      2. Schedules missing iterations (i.e. gaps between 1 and iterations) by using the scheduler.
      3. Sorts the CSV file.
      4. Updates overall benchmark statistics.

    Parameters:
        size (int): The array size to test.
        iterations (int): Total iterations desired per algorithm.
        threshold (float): Performance threshold in seconds (also used as the timeout if enabled).
        expected_algs (list): List of algorithm names.
        overall_totals (dict): Aggregated totals dictionary.
        per_alg_results (dict): Per-algorithm performance records.
        skip_list (dict): Mapping of algorithms to the size at which they were skipped.
        per_run_timeout (bool): If True, enforce per-iteration timeouts.

    Returns:
        tuple: Updated (size_results, skip_list).
    """
    csv_path, size_results, max_iters = get_csv_results_for_size(size, expected_algs)
    current_workers = get_num_workers()

    # Update worker count if changed.
    process_size.workers = getattr(process_size, "workers", None)
    if process_size.workers is None or current_workers != process_size.workers:
        if process_size.workers is None:
            print(
                f"Using {current_workers} worker{'s' if current_workers > 1 else ''}."
            )
        else:
            print(
                f"Changing workers from {process_size.workers} to {current_workers} worker{'s' if current_workers > 1 else ''}."
            )
        process_size.workers = current_workers

    # Schedule missing iterations (fill gaps) for each algorithm.
    size_results, skip_list = update_missing_iterations_concurrent(
        csv_path,
        size,
        expected_algs,
        size_results,
        iterations,
        skip_list,
        threshold,
        current_workers,
        per_run_timeout,
        max_iters,
    )
    sort_csv_alphabetically(csv_path)
    # Re-read the updated CSV file.
    _, updated_results, _ = get_csv_results_for_size(size, expected_algs)
    update_overall_results(
        size,
        updated_results,
        expected_algs,
        overall_totals,
        per_alg_results,
        iterations,
    )
    return size_results, skip_list


def run_sorting_tests(iterations=500, threshold=300, per_run_timeout=False):
    """
    Execute benchmark tests across multiple array sizes and generate reports.

    This function performs the following steps:
      1. Generate the array sizes.
      2. Initialize overall statistics and per-algorithm records.
      3. For each array size:
           a. Process missing iterations.
           b. Write a per-size markdown report.
           c. Rebuild the main README with updated overall statistics.
      4. Generate individual markdown reports for each algorithm.

    Parameters:
        iterations (int): Number of iterations per algorithm per array size.
        threshold (float): Performance threshold (in seconds) for skipping an algorithm (and used as timeout if enabled).
        per_run_timeout (bool): If True, enforce per-iteration timeouts (using threshold as timeout).

    Returns:
        None
    """
    sizes = generate_sizes()
    expected_algs = list(get_algorithms().keys())
    overall_totals = {alg: {"sum": 0, "count": 0} for alg in expected_algs}
    per_alg_results = {alg: [] for alg in expected_algs}
    skip_list = {}
    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)
    details_path = "details.md"
    with open(details_path, "w") as f:
        f.write("")
    initial_workers = get_num_workers()
    print(f"Using {initial_workers} worker{'s' if initial_workers > 1 else ''}.")
    process_size.workers = initial_workers

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
            per_run_timeout=per_run_timeout,
        )
        # Mark algorithms whose average exceeds the threshold as skipped.
        for alg, data in size_results.items():
            if data is not None and data[0] > threshold and alg not in skip_list:
                skip_list[alg] = size
        with open(details_path, "a") as f:
            write_markdown(f, size, size_results, skip_list)
        rebuild_readme(overall_totals, details_path, skip_list)

    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

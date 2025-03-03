"""
processor.py

This module coordinates the processing of benchmark tests for various array sizes.
It handles:
  - Updating overall benchmark results.
  - Processing individual array sizes.
  - Running the complete benchmark test cycle and generating reports.
  
Functions:
    update_overall_results(size, size_results, expected_algs, overall_totals, per_alg_results, iterations)
    process_size(size, iterations, threshold, expected_algs, overall_totals, per_alg_results, skip_list, per_run_timeout=False)
    run_sorting_tests(iterations=500, threshold=300, per_run_timeout=False)
"""

import os
import sys
from csv_utils import get_csv_results_for_size, sort_csv_alphabetically
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown
from benchmark import (
    generate_sizes,
    get_num_workers,
    update_missing_iterations_concurrent,
)
from exit_handlers import shutdown_requested


def update_overall_results(
    size, size_results, expected_algs, overall_totals, per_alg_results, iterations
):
    """
    Update aggregated benchmark results for a specific array size.

    For each algorithm, this function updates:
      - The cumulative sum (average * iterations).
      - The total iteration count.
      - The per-algorithm results list with current statistics.

    Parameters:
        size (int): The current array size.
        size_results (dict): Mapping from algorithm to performance tuple.
        expected_algs (list): List of expected algorithm names.
        overall_totals (dict): Dictionary to accumulate overall results.
        per_alg_results (dict): Dictionary storing individual algorithm performance per size.
        iterations (int): Total iterations expected per algorithm.
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

    Retrieves or creates the CSV file for the given size, updates missing iterations,
    sorts the CSV, and updates overall performance metrics.

    Parameters:
        size (int): The current array size.
        iterations (int): Total iterations per algorithm.
        threshold (float): Time threshold to decide if an algorithm should be skipped.
        expected_algs (list): List of algorithm names.
        overall_totals (dict): Aggregated performance metrics.
        per_alg_results (dict): Performance records per algorithm.
        skip_list (dict): Dictionary of algorithms to be skipped (with the size at which they were skipped).
        per_run_timeout (bool): Flag to enable per-iteration timeout.

    Returns:
        tuple: Updated (size_results, skip_list).
    """
    # Retrieve CSV file path and existing results (ignore extra returned values).
    result = get_csv_results_for_size(size, expected_algs)
    csv_path, size_results, *_ = result

    # Determine the number of worker processes.
    current_workers = get_num_workers()
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
        per_run_timeout,
    )
    # Sort the CSV file for consistency.
    sort_csv_alphabetically(csv_path)
    # Re-read the updated CSV to update overall results.
    result = get_csv_results_for_size(size, expected_algs)
    _, updated_results, *_ = result
    update_overall_results(
        size,
        updated_results,
        expected_algs,
        overall_totals,
        per_alg_results,
        iterations,
    )

    # Mark algorithms that exceed the threshold for skipping in future sizes.
    for alg, data in updated_results.items():
        if data is not None and data[0] > threshold and alg not in skip_list:
            skip_list[alg] = size
    return size_results, skip_list


def run_sorting_tests(iterations=500, threshold=300, per_run_timeout=False):
    """
    Run benchmark tests across multiple array sizes and generate reports.

    This function:
      - Generates array sizes.
      - Iterates over each size to process benchmark tests.
      - Updates CSV files and markdown reports.
      - Builds an overall README with aggregated results.

    Parameters:
        iterations (int): Number of iterations per algorithm per array size.
        threshold (float): Time threshold in seconds to decide if an algorithm should be skipped.
        per_run_timeout (bool): Whether to enforce a timeout for each iteration.
    """
    from algorithms_map import (
        get_algorithms,
    )  # Local import for expected algorithm mapping.

    sizes = generate_sizes()
    expected_algs = list(get_algorithms().keys())
    overall_totals = {alg: {"sum": 0, "count": 0} for alg in expected_algs}
    per_alg_results = {alg: [] for alg in expected_algs}
    skip_list = {}
    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)
    details_path = "details.md"
    # Clear previous details file.
    with open(details_path, "w") as f:
        f.write("")
    initial_workers = get_num_workers()
    print(f"Using {initial_workers} worker{'s' if initial_workers > 1 else ''}.")
    process_size.workers = initial_workers

    try:
        for size in sizes:
            if shutdown_requested:
                print("Shutdown requested. Exiting the size loop.")
                sys.exit(0)
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
            # Check to skip algorithms that exceed the time threshold.
            for alg, data in size_results.items():
                if data is not None and data[0] > threshold and alg not in skip_list:
                    skip_list[alg] = size
            # Append per-size markdown details.
            with open(details_path, "a") as f:
                write_markdown(f, size, size_results, skip_list)
            # Rebuild the overall README using updated totals.
            rebuild_readme(overall_totals, details_path, skip_list)
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting gracefully.")
        sys.exit(0)

    # Generate individual markdown reports for each algorithm.
    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

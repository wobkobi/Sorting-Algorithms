"""
processor.py

Coordinates benchmark test processing for various array sizes.

Handles:
  - Updating overall benchmark results.
  - Processing benchmarks for each array size.
  - Generating reports (CSV, markdown, README).

Functions:
  - update_overall_results(): Update aggregated results for a size.
  - process_size(): Process benchmarks for one array size.
  - run_sorting_tests(): Execute the complete benchmark cycle.
"""

import os
import sys
from benchmark.csv_utils import get_csv_results_for_size, sort_csv_alphabetically
from benchmark.markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown
from benchmark import (
    generate_sizes,
    get_num_workers,
    update_missing_iterations_concurrent,
)
from benchmark.exit_handlers import shutdown_requested


def update_overall_results(
    size, size_results, expected_algs, overall_totals, per_alg_results, iterations
):
    """
    Update aggregated benchmark results for a specific array size.

    For each algorithm, the function updates the cumulative time sum and count,
    and records the per-size performance statistics.

    Parameters:
      size (int): Current array size.
      size_results (dict): Mapping from algorithm to performance tuple.
      expected_algs (list): List of expected algorithm names.
      overall_totals (dict): Accumulated overall results.
      per_alg_results (dict): Per-algorithm results by array size.
      iterations (int): Number of iterations per algorithm.
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

    Retrieves or creates the CSV file for the size, updates missing iterations,
    sorts the CSV, and updates overall performance metrics. Also marks algorithms
    exceeding the time threshold for skipping.

    Parameters:
      size (int): Current array size.
      iterations (int): Total iterations per algorithm.
      threshold (float): Time threshold (seconds) to skip slow algorithms.
      expected_algs (list): List of algorithm names.
      overall_totals (dict): Aggregated performance metrics.
      per_alg_results (dict): Per-algorithm performance records.
      skip_list (dict): Algorithms to skip (keyed by algorithm name).
      per_run_timeout (bool): Enable per-iteration timeout if True.

    Returns:
      tuple: (size_results, skip_list)
    """
    # Retrieve CSV file and current results.
    csv_path, size_results, *_ = get_csv_results_for_size(size, expected_algs)

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
    # Sort CSV for consistency.
    sort_csv_alphabetically(csv_path)
    # Re-read updated CSV and update overall results.
    _, updated_results, *_ = get_csv_results_for_size(size, expected_algs)
    update_overall_results(
        size,
        updated_results,
        expected_algs,
        overall_totals,
        per_alg_results,
        iterations,
    )

    # Mark algorithms exceeding the threshold for skipping.
    for alg, data in updated_results.items():
        if data is not None and data[0] > threshold and alg not in skip_list:
            skip_list[alg] = size
    return size_results, skip_list


def run_sorting_tests(iterations=500, threshold=300, per_run_timeout=False):
    """
    Run benchmark tests across multiple array sizes and generate reports.

    The function:
      - Generates array sizes.
      - Processes benchmarks for each size.
      - Updates CSV files and markdown reports.
      - Rebuilds the overall README.md file.

    Parameters:
      iterations (int): Number of iterations per algorithm for each size.
      threshold (float): Time threshold (seconds) to determine skipping.
      per_run_timeout (bool): Enforce a timeout for each iteration if True.
    """
    from benchmark.algorithms_map import get_algorithms  # Local import for mapping.

    sizes = generate_sizes()
    expected_algs = list(get_algorithms().keys())
    overall_totals = {alg: {"sum": 0, "count": 0} for alg in expected_algs}
    per_alg_results = {alg: [] for alg in expected_algs}
    skip_list = {}
    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)
    details_path = "details.md"
    # Clear previous details.
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
            # Mark slow algorithms for skipping.
            for alg, data in size_results.items():
                if data is not None and data[0] > threshold and alg not in skip_list:
                    skip_list[alg] = size
            # Append markdown details for this size.
            with open(details_path, "a") as f:
                write_markdown(f, size, size_results, skip_list)
            # Rebuild overall README.
            rebuild_readme(overall_totals, details_path, skip_list)
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting gracefully.")
        sys.exit(0)

    # Generate individual algorithm markdown reports.
    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

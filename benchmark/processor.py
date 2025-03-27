"""
processor.py

Coordinates benchmark test processing for various array sizes.
Handles processing for each array size, updates overall results,
and generates reports (CSV, markdown, README).
This version also tracks the processing time for each array size
and writes runtime stats immediately to a JSON file.
"""

import os
import sys
import datetime
from .utils import format_size
from .csv_utils import get_csv_results_for_size, sort_csv_alphabetically
from .markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown
from .sizes import generate_sizes, get_num_workers
from .scheduler import update_missing_iterations_concurrent
from .exit_handlers import shutdown_requested
from .algorithms_map import get_algorithms
from . import config  # Import config module to update its runtime globals
from .config import debug


def update_overall_results(
    size, size_results, expected_algs, overall_totals, per_alg_results, iterations
):
    """
    Update aggregated benchmark results for a given array size.

    Parameters:
      size (int): Array size.
      size_results (dict): Performance results for this size.
      expected_algs (list): List of algorithm names.
      overall_totals (dict): Cumulative performance totals.
      per_alg_results (dict): Per–algorithm results.
      iterations (int): Number of iterations per algorithm.
    """
    debug(f"Updating overall results for array size {format_size(size)}.")
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

    Retrieves CSV results, updates missing iterations concurrently,
    sorts CSV rows, updates overall performance, and marks slow algorithms.

    Parameters:
      size (int): Current array size.
      iterations (int): Iterations per algorithm.
      threshold (float): Time threshold.
      expected_algs (list): Algorithm names.
      overall_totals (dict): Cumulative totals.
      per_alg_results (dict): Per–algorithm results.
      skip_list (dict): Algorithms to skip.
      per_run_timeout (bool): Whether to enable per–iteration timeouts.

    Returns:
      tuple: (size_results, updated skip_list)
    """
    debug(
        f"Processing array size {format_size(size)} with {iterations} iterations and threshold {threshold}."
    )
    csv_path, size_results, _ = get_csv_results_for_size(
        size, expected_algs, max_iterations=iterations
    )
    current_workers = get_num_workers()
    process_size.workers = getattr(process_size, "workers", None)
    if process_size.workers is None or current_workers != process_size.workers:
        if process_size.workers is None:
            print(
                f"Using {current_workers} worker{'s' if current_workers > 1 else ''}."
            )
            debug(f"Initial worker count: {current_workers}.")
        else:
            print(
                f"Changing workers from {process_size.workers} to {current_workers} worker{'s' if current_workers > 1 else ''}."
            )
            debug(
                f"Worker count changed from {process_size.workers} to {current_workers}."
            )
        process_size.workers = current_workers

    size_results, skip_list = update_missing_iterations_concurrent(
        csv_path,
        size,
        expected_algs,
        size_results,
        iterations,
        skip_list,
        threshold,
        current_workers,
        per_run_timeout=per_run_timeout,
    )
    sort_csv_alphabetically(csv_path)
    _, updated_results, _ = get_csv_results_for_size(
        size, expected_algs, max_iterations=iterations
    )
    update_overall_results(
        size,
        updated_results,
        expected_algs,
        overall_totals,
        per_alg_results,
        iterations,
    )

    for alg, data in updated_results.items():
        if data is not None and data[0] > threshold and alg not in skip_list:
            skip_list[alg] = size
            debug(
                f"Algorithm {alg} exceeded threshold at size {format_size(size)}. Marked for skipping."
            )
    return size_results, skip_list


def run_sorting_tests(iterations=500, threshold=300, per_run_timeout=False):
    """
    Run benchmark tests across multiple array sizes and generate reports.

    This function generates array sizes, processes each size, updates CSV files,
    generates markdown details, rebuilds the README, and creates per–algorithm reports.
    It also records and immediately writes the runtime for each array size to a JSON file.

    Parameters:
      iterations (int): Number of iterations per algorithm.
      threshold (float): Time threshold.
      per_run_timeout (bool): Whether to enforce timeouts on iterations.
    """
    # Update runtime tracking variables directly on the config module.
    config.RUN_START_TIME = datetime.datetime.now()
    debug("Run start time set.")

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
    process_size.workers = get_num_workers()
    print(
        f"Using {process_size.workers} worker{'s' if process_size.workers > 1 else ''}."
    )
    debug(f"Initial worker count: {process_size.workers}.")

    for size in sizes:
        if shutdown_requested:
            print("Shutdown requested. Exiting the size loop.")
            debug("Shutdown requested. Exiting loop in run_sorting_tests.")
            break

        # Update current array tracking on config.
        config.CURRENT_ARRAY = size
        config.CURRENT_ARRAY_START = datetime.datetime.now()

        print(f"\nTesting array size: {format_size(size)}")
        debug(f"Testing array size: {format_size(size)}")
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
        for alg, data in size_results.items():
            if data is not None and data[0] > threshold and alg not in skip_list:
                skip_list[alg] = size
                debug(
                    f"Algorithm {alg} exceeded threshold at size {format_size(size)}. Marked for skipping."
                )
        with open(details_path, "a") as f:
            write_markdown(f, size, size_results, skip_list)
        rebuild_readme(overall_totals, details_path, skip_list)
        # Update worker count if needed.
        current_workers = get_num_workers()
        if process_size.workers != current_workers:
            print(
                f"Updating worker count from {process_size.workers} to {current_workers} worker{'s' if current_workers > 1 else ''}."
            )
            debug(
                f"Worker count updated from {process_size.workers} to {current_workers}."
            )
            process_size.workers = current_workers

        # Compute elapsed time for this array size.
        elapsed = (datetime.datetime.now() - config.CURRENT_ARRAY_START).total_seconds()
        config.ARRAY_TIME_LOG.append((size, elapsed))
        debug(f"Array size {format_size(size)} processed in {elapsed:.2f} seconds.")
        # Immediately save runtime stats to JSON.
        from .exit_handlers import save_runtime_log_json

        save_runtime_log_json()
        # Clear current array tracking.
        config.CURRENT_ARRAY = None
        config.CURRENT_ARRAY_START = None

    try:
        write_algorithm_markdown(per_alg_results)
        print(
            "\nBenchmark complete: CSV files saved, README.md updated, and per–algorithm files created in 'results/algorithms'."
        )
        debug("Completed run_sorting_tests.")
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting gracefully.")
        debug("KeyboardInterrupt caught in run_sorting_tests. Exiting.")
        sys.exit(0)

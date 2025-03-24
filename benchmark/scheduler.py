"""
scheduler.py

Provides functions to safely run sorting iterations and schedule missing iterations concurrently.
Includes:
  - safe_run_target(): Runs a single iteration in a separate process.
  - safe_run_iteration(): Runs an iteration with a timeout.
  - update_missing_iterations_concurrent(): Schedules and processes missing iterations.

This version has been updated to avoid recording DNFs if a shutdown is detected.
"""

import csv
import sys
import os
from multiprocessing import Pipe, Process
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from .exit_handlers import shutdown_requested
from .utils import (
    format_size,
    run_iteration,
    compute_average,
    compute_median,
    format_time,
)
from .algorithms_map import get_algorithms
from .config import debug


def safe_run_target(conn, sort_func, size):
    """
    Run a single sorting iteration and send the result through a Pipe.

    Parameters:
      conn: Multiprocessing Pipe connection.
      sort_func (callable): Sorting function to run.
      size (int): Array size.
    """
    debug(f"safe_run_target: Running {sort_func.__name__} on size {size}.")
    try:
        result = run_iteration(sort_func, size)
        conn.send(result)
    except Exception as e:
        conn.send(e)
    finally:
        conn.close()
        debug(f"safe_run_target: Finished {sort_func.__name__} on size {size}.")


def safe_run_iteration(sort_func, size, timeout):
    """
    Execute a sorting iteration in a separate process with a timeout.

    Parameters:
      sort_func (callable): Sorting function.
      size (int): Array size.
      timeout (float): Timeout in seconds.

    Returns:
      float or None: Elapsed time if successful, None otherwise.
    """
    debug(
        f"safe_run_iteration: Starting {sort_func.__name__} on size {size} with timeout {timeout}."
    )
    parent_conn, child_conn = Pipe()
    p = Process(target=safe_run_target, args=(child_conn, sort_func, size))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        debug(f"safe_run_iteration: {sort_func.__name__} on size {size} timed out.")
        return None
    if parent_conn.poll():
        res = parent_conn.recv()
        debug(
            f"safe_run_iteration: {sort_func.__name__} on size {size} returned {res}."
        )
        return None if isinstance(res, Exception) else res
    return None


def update_missing_iterations_concurrent(
    csv_path,
    size,
    expected_algs,
    size_results,
    iterations,
    skip_list,
    threshold,
    num_workers,
    per_run_timeout=False,
):
    """
    Schedule and execute missing iterations concurrently for each algorithm.

    If shutdown is detected, processing is aborted and remaining iterations are not marked as DNF.

    Parameters:
      csv_path (str): Path to the CSV file.
      size (int): Array size.
      expected_algs (list): List of algorithm names.
      size_results (dict): In-memory results for the size.
      iterations (int): Total iterations per algorithm.
      skip_list (dict): Algorithms to skip.
      threshold (float): Time threshold.
      num_workers (int): Number of worker processes.
      per_run_timeout (bool): Whether to enable timeouts.

    Returns:
      tuple: (updated size_results, updated skip_list)
    """
    debug(
        f"update_missing_iterations_concurrent: Processing missing iterations for size {format_size(size)}."
    )
    # PART 1: Build mapping of existing iterations from CSV.
    existing_iters = {alg: set() for alg in expected_algs}
    try:
        with open(csv_path, "r", newline="") as f:
            reader = csv.reader(f)
            next(reader, None)  # Skip header.
            for row in reader:
                if not row or len(row) < 4:
                    continue
                alg_name = row[0]
                try:
                    iter_num = int(row[2])
                except Exception:
                    continue
                if alg_name in existing_iters:
                    existing_iters[alg_name].add(iter_num)
    except Exception as e:
        debug(f"Error reading CSV {csv_path}: {e}")

    # PART 2: Determine missing iterations.
    missing_algs = {}
    for alg in expected_algs:
        if alg in skip_list:
            continue
        current_iters = existing_iters.get(alg, set())
        missing = sorted(set(range(1, iterations + 1)) - current_iters)
        if missing:
            missing_algs[alg] = missing

    if missing_algs:
        debug(f"Algorithms with no results yet: {', '.join(missing_algs.keys())}.")
    else:
        debug("No missing iterations found.")
        return size_results, skip_list

    completed_counts = {}
    tasks = {}
    ExecutorClass = ThreadPoolExecutor if per_run_timeout else ProcessPoolExecutor

    with ExecutorClass(max_workers=num_workers) as executor:
        for alg, missing_list in missing_algs.items():
            for iter_num in missing_list:
                if shutdown_requested:
                    debug(
                        "Shutdown requested during task scheduling. Aborting further submissions."
                    )
                    break
                if per_run_timeout:
                    future = executor.submit(
                        safe_run_iteration, get_algorithms()[alg], size, threshold
                    )
                else:
                    future = executor.submit(run_iteration, get_algorithms()[alg], size)
                tasks[future] = (alg, iter_num)
        debug(f"Scheduled {len(tasks)} tasks for missing iterations.")

        # Process task results.
        for future in as_completed(tasks):
            if shutdown_requested:
                debug(
                    "Shutdown requested, aborting remaining iteration writes without recording DNF."
                )
                break
            alg, iter_num = tasks[future]
            completed_counts[alg] = completed_counts.get(alg, 0) + 1
            try:
                t = future.result()
                debug(f"Task complete for {alg} iteration {iter_num}: result={t}")
            except Exception as e:
                debug(f"Task error for {alg} iteration {iter_num}: {e}")
                t = None

            # Check shutdown again before writing.
            if shutdown_requested:
                debug("Shutdown requested before writing CSV; skipping row write.")
                break

            try:
                with open(csv_path, "a", newline="") as csv_file:
                    writer = csv.writer(csv_file)
                    row = [alg, size, iter_num, "DNF" if t is None else f"{t:.8f}"]
                    writer.writerow(row)
                    csv_file.flush()
                    os.fsync(csv_file.fileno())
                debug(f"Wrote row to CSV: {row}")
            except Exception as e:
                debug(f"Error writing row for {alg} iteration {iter_num}: {e}")

            # Update in-memory results.
            if size_results.get(alg) is None:
                size_results[alg] = (None, None, None, None, 0, [])
            old_times = size_results[alg][5]
            if isinstance(old_times, list):
                old_times = {i + 1: old_times[i] for i in range(len(old_times))}
            old_times[iter_num] = t
            new_count = len(old_times)
            size_results[alg] = (None, None, None, None, new_count, old_times)

            if completed_counts[alg] == len(missing_algs.get(alg, [])):
                times_dict = size_results[alg][5]
                times_list = [times_dict[k] for k in sorted(times_dict.keys())]
                successful_times = [x for x in times_list if x is not None]
                dnf_count = len(times_list) - len(successful_times)
                if successful_times:
                    avg = compute_average(successful_times)
                    median = compute_median(successful_times)
                    min_time = min(successful_times)
                    max_time = max(successful_times)
                else:
                    avg = float("inf")
                    median = None
                    min_time = None
                    max_time = None
                size_results[alg] = (
                    avg,
                    min_time,
                    max_time,
                    median,
                    len(times_list),
                    times_list,
                )
                debug(
                    f"Final stats for {alg} on size {format_size(size)}: avg={avg}, count={len(times_list)}, DNF={dnf_count}"
                )

    return size_results, skip_list

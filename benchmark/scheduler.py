"""
scheduler.py

Provides functions to safely run sorting iterations and schedule missing iterations concurrently.

Features:
  - Running individual iterations in separate processes with optional timeouts.
  - Scheduling missing iterations using concurrent futures.
  - Writing iteration results immediately to CSV with data persistence.

Functions:
  - safe_run_target(): Runs a single iteration and sends back the result.
  - safe_run_iteration(): Executes a single iteration with a timeout.
  - update_missing_iterations_concurrent(): Schedules missing iterations concurrently.
"""

import csv
import sys
import os
from multiprocessing import Pipe, Process
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from .exit_handlers import shutdown_requested
from .utils import format_size, run_iteration, compute_average, compute_median, format_time
from .algorithms_map import get_algorithms
from .config import debug


def safe_run_target(conn, sort_func, size):
    """
    Run a single sorting iteration and send the result through a Pipe connection.

    Intended to run in a separate process so it can be terminated if needed.

    Parameters:
      conn (Connection): Pipe connection for sending back the result.
      sort_func (callable): Sorting function to execute.
      size (int): Array size for the iteration.
    """
    try:
        result = run_iteration(sort_func, size)
        conn.send(result)
    except Exception as e:
        conn.send(e)
    finally:
        conn.close()


def safe_run_iteration(sort_func, size, timeout):
    """
    Execute a sorting iteration in a separate process with a timeout.

    If the iteration exceeds the timeout, it is terminated and returns None.

    Parameters:
      sort_func (callable): Sorting function to execute.
      size (int): Array size for the iteration.
      timeout (float): Maximum allowed time in seconds.

    Returns:
      float or None: Elapsed time if completed in time, otherwise None.
    """
    parent_conn, child_conn = Pipe()
    p = Process(target=safe_run_target, args=(child_conn, sort_func, size))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        return None
    if parent_conn.poll():
        res = parent_conn.recv()
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
    Schedule and execute missing iterations concurrently for each sorting algorithm.

    The function:
      1. Reads the CSV to determine which iterations exist.
      2. Identifies missing iteration numbers per algorithm.
      3. Schedules tasks for missing iterations.
      4. Writes each iteration result immediately to the CSV.
      5. Updates in-memory results and computes final statistics.

    Parameters:
      csv_path (str): Full path to the CSV file for the current array size.
      size (int): Current array size.
      expected_algs (list): List of expected algorithm names.
      size_results (dict): Current in-memory benchmark results.
      iterations (int): Total iterations per algorithm.
      skip_list (dict): Algorithms to skip (keyed by algorithm name).
      threshold (float): Time threshold to determine if an algorithm should be skipped.
      num_workers (int): Number of worker processes to use.
      per_run_timeout (bool): Enable per-iteration timeout if True.

    Returns:
      tuple: (updated size_results, updated skip_list)
    """
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

    # PART 2: Determine missing iterations for each algorithm.
    missing_algs = {}
    for alg in expected_algs:
        if alg in skip_list:
            continue
        current_iters = existing_iters.get(alg, set())
        missing = sorted(set(range(1, iterations + 1)) - current_iters)
        if missing:
            missing_algs[alg] = missing

    # PART 3: Print status messages.
    if missing_algs:
        found_msgs = []
        not_run_msgs = []
        for alg in missing_algs:
            data = size_results.get(alg)
            if data is not None:
                current = data[4] if len(data) >= 5 else 0
                found_msgs.append(
                    alg
                    if current == 0 or current == iterations
                    else f"{alg} ({current})"
                )
            else:
                not_run_msgs.append(alg)
        if found_msgs:
            max_items = min(10, len(found_msgs))
            disp = ", ".join(found_msgs[:max_items])
            if len(found_msgs) > max_items:
                disp += f", and {len(found_msgs)-max_items} more..."
            print(f"Algorithms with partial/complete results: {disp}.")
        if not_run_msgs:
            max_items = min(10, len(not_run_msgs))
            disp = ", ".join(not_run_msgs[:max_items])
            if len(not_run_msgs) > max_items:
                disp += f", and {len(not_run_msgs)-max_items} more..."
            print(f"Algorithms with no results yet: {disp}.")
    else:
        return size_results, skip_list

    # PART 4: Schedule tasks using a concurrent executor.
    completed_counts = {}
    tasks = {}
    ExecutorClass = ThreadPoolExecutor if per_run_timeout else ProcessPoolExecutor

    with ExecutorClass(max_workers=num_workers) as executor:
        for alg, missing_list in missing_algs.items():
            for iter_num in missing_list:
                if shutdown_requested:
                    print("Shutdown requested. Exiting immediately.")
                    sys.exit(0)
                if per_run_timeout:
                    future = executor.submit(
                        safe_run_iteration, get_algorithms()[alg], size, threshold
                    )
                else:
                    future = executor.submit(run_iteration, get_algorithms()[alg], size)
                tasks[future] = (alg, iter_num)
        debug(f"Scheduled {len(tasks)} tasks for missing iterations.")

        # PART 5: Process task results and write each result immediately to CSV.
        for future in as_completed(tasks):
            if shutdown_requested:
                for f in tasks:
                    f.cancel()
                print("Shutdown requested during task processing. Exiting loop.")
                sys.exit(0)
            alg, iter_num = tasks[future]
            completed_counts[alg] = completed_counts.get(alg, 0) + 1
            try:
                t = future.result()
                debug(f"Task complete for {alg} iteration {iter_num}: result={t}")
            except Exception as e:
                print(f"{alg} error on size {size} iteration {iter_num}: {e}")
                t = None

            # Write the result to CSV immediately.
            try:
                with open(csv_path, "a", newline="") as csv_file:
                    writer = csv.writer(csv_file)
                    row = [alg, size, iter_num, "DNF" if t is None else f"{t:.8f}"]
                    writer.writerow(row)
                    csv_file.flush()
                    os.fsync(csv_file.fileno())
                debug(f"Wrote row to CSV: {row}")
            except Exception as e:
                print(f"Error writing {alg} iteration {iter_num} to CSV: {e}")

            # Update in-memory results.
            if size_results.get(alg) is None:
                size_results[alg] = (None, None, None, None, 0, [])
            old_times = size_results[alg][5]
            if isinstance(old_times, list):
                old_times = {i + 1: old_times[i] for i in range(len(old_times))}
            old_times[iter_num] = t
            new_count = len(old_times)
            size_results[alg] = (None, None, None, None, new_count, old_times)

            # Compute final statistics once all missing iterations for an algorithm are complete.
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
                print(
                    f"{alg} on size {format_size(size)}: {format_time(avg, False)} "
                    + (f"(DNF: {dnf_count})" if dnf_count > 0 else "")
                )
    return size_results, skip_list

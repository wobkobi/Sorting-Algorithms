"""
This module contains functions for safely running individual sorting iterations
and scheduling missing iterations concurrently.

It supports enforcing a timeout on each iteration by running the sort in a separate process.
Missing iteration numbers (i.e. gaps in the CSV file) are detected and scheduled for execution.
"""

import csv
from multiprocessing import Pipe, Process
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed
from algorithms_map import get_algorithms
from utils import compute_average, compute_median, format_time, run_iteration

# Global flag to support graceful shutdown (if needed)
shutdown_requested = False


def safe_run_target(conn, sort_func, size):
    """
    Execute a single sorting iteration in a separate process and send the result via a pipe.

    This function is intended to be run in its own process so that a timeout can be enforced.
    It calls the provided sorting function (or an alternative iteration function) and sends back
    the elapsed time (or any exception encountered).

    Parameters:
        conn: The connection (pipe) object used to send back the result.
        sort_func (callable): The sorting function to be executed.
        size (int): The size of the array to sort.

    Returns:
        None: The result (or exception) is sent back through the pipe.
    """
    try:
        # Optionally, you can use run_iteration(sort_func, size) if you want to measure the runtime.
        result = sort_func(list(range(size)))
        conn.send(result)
    except Exception as e:
        conn.send(e)
    finally:
        conn.close()


def safe_run_iteration(sort_func, size, timeout):
    """
    Execute a sorting iteration with a timeout.

    A new process is spawned to run the sorting iteration using safe_run_target.
    If the process does not finish within the specified timeout, it is terminated
    and the iteration is considered a DNF (returns None).

    Parameters:
        sort_func (callable): The sorting function to execute.
        size (int): The size of the array to sort.
        timeout (float): Maximum allowed time (in seconds) for the iteration.

    Returns:
        float or None: The elapsed time if the iteration completes within the timeout;
                       otherwise, None (indicating a timeout/ DNF).
    """
    parent_conn, child_conn = Pipe()
    p = Process(target=safe_run_target, args=(child_conn, sort_func, size))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        return None  # Did Not Finish within the timeout.
    if parent_conn.poll():
        res = parent_conn.recv()
        # If an exception was sent, treat it as a timeout (DNF).
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
    max_iters=None,
):
    """
    Schedule and execute missing iterations concurrently for each algorithm.

    This function first reads the CSV file (or the in-memory results) to determine which
    iteration numbers (from 1 up to the desired 'iterations') are missing for each algorithm.
    It then schedules tasks to execute only those missing iterations. If per_run_timeout is True,
    each iteration is given a timeout equal to the threshold value.

    Parameters:
        csv_path (str): Path to the CSV file for the current array size.
        size (int): The current array size being benchmarked.
        expected_algs (list): List of algorithm names.
        size_results (dict): In-memory results for the current size (as returned by read_csv_results).
        iterations (int): Total iterations desired per algorithm (e.g., 500).
        skip_list (dict): Mapping of algorithms to the size at which they were skipped (for future sizes).
        threshold (float): The performance threshold (in seconds) used both for skipping and as a timeout if enabled.
        num_workers (int): The number of worker processes available for concurrent execution.
        per_run_timeout (bool): If True, enforce a timeout on each iteration using 'threshold' as timeout.
        max_iters (dict): Optional mapping of algorithm names to the highest iteration number already recorded.

    Returns:
        tuple: Updated size_results and skip_list.
    """
    # Compute missing iteration numbers for each algorithm.
    missing_algs = {}
    for alg in expected_algs:
        if alg in skip_list:
            continue
        # Retrieve the set of iteration numbers already recorded for this algorithm.
        current_iter_set = size_results.get(
            alg, (None, None, None, None, 0, {}, set())
        )[6]
        # Compute the set difference between desired iteration numbers and those recorded.
        missing_iters = sorted(set(range(1, iterations + 1)) - current_iter_set)
        if missing_iters:
            missing_algs[alg] = missing_iters

    # Print status messages for missing iterations.
    for alg, missing_list in missing_algs.items():
        if not size_results.get(alg) or size_results[alg][4] == 0:
            print(
                f"{alg} has no iterations yet; scheduling {len(missing_list)} iterations."
            )
        else:
            print(f"{alg} needs {len(missing_list)} additional iterations.")

    if not missing_algs:
        return size_results, skip_list

    completed_counts = (
        {}
    )  # Track the number of missing iterations completed per algorithm.
    tasks = {}

    # Choose the executor based on whether timeouts are enabled.
    ExecutorClass = ThreadPoolExecutor if per_run_timeout else ProcessPoolExecutor
    executor_workers = min(num_workers, 2) if per_run_timeout else num_workers

    with ExecutorClass(max_workers=executor_workers) as executor:
        for alg, missing_list in missing_algs.items():
            # Schedule tasks for each missing iteration number.
            for iter_num in missing_list:
                if per_run_timeout:
                    future = executor.submit(
                        safe_run_iteration, get_algorithms()[alg], size, threshold
                    )
                else:
                    future = executor.submit(run_iteration, get_algorithms()[alg], size)
                tasks[future] = (alg, iter_num)

        # Process each task as it completes.
        for future in as_completed(tasks):
            alg, iter_num = tasks[future]
            completed_counts[alg] = completed_counts.get(alg, 0) + 1
            try:
                t = future.result()
            except Exception as e:
                print(f"{alg} error on size {size} iteration {iter_num}: {e}")
                t = None
            # Write the result to the CSV file.
            with open(csv_path, "a", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(
                    [alg, size, iter_num, "DNF" if t is None else f"{t:.8f}"]
                )
            # Update in-memory results: ensure there is a dictionary for times.
            if size_results.get(alg) is None:
                size_results[alg] = (None, None, None, None, 0, {}, set())
            # Unpack current data.
            _, _, _, _, count, times_dict, iter_set = size_results[alg]
            # Record the result for this iteration.
            times_dict[iter_num] = t
            iter_set.add(iter_num)
            count += 1
            size_results[alg] = (None, None, None, None, count, times_dict, iter_set)
            # Once all missing iterations for this algorithm are processed, compute statistics.
            if completed_counts[alg] == len(missing_algs.get(alg, [])):
                sorted_iters = sorted(times_dict.keys())
                times_list = [times_dict[i] for i in sorted_iters]
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
                # Update the result tuple for this algorithm.
                size_results[alg] = (
                    avg,
                    min_time,
                    max_time,
                    median,
                    len(times_list),
                    times_list,
                    set(sorted_iters),
                )
                print(
                    f"Average for {alg} on size {size}: {format_time(avg, False)}"
                    + (
                        f" (DNF: {dnf_count}/{len(times_list)})"
                        if dnf_count > 0
                        else ""
                    )
                )
                # If the algorithm's performance is below threshold or too many DNFs, mark it for skipping.
                if (
                    avg > threshold
                    or (len(times_list) > 0 and dnf_count / len(times_list) >= 0.5)
                ) and alg not in skip_list:
                    skip_list[alg] = size
                    print(
                        f"Skipping {alg} for future sizes (avg > threshold or high DNF ratio, skipped at size {size})."
                    )
    return size_results, skip_list

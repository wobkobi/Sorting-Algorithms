import csv
import sys
from multiprocessing import Pipe, Process
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed
from exit_handlers import shutdown_requested
from utils import run_iteration, compute_average, compute_median, format_time
from algorithms_map import get_algorithms


def safe_run_target(conn, sort_func, size):
    """
    Run a single iteration of a sorting algorithm and send its result via a connection.
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
    Execute a sorting iteration with a timeout using a separate process.
    Returns the elapsed time if finished in time; otherwise, None.
    """
    parent_conn, child_conn = Pipe()
    p = Process(target=safe_run_target, args=(child_conn, sort_func, size))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        return None  # Timeout: Did Not Finish
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
    Schedule and execute missing iterations for each algorithm concurrently.
    """
    # Read existing iteration numbers from CSV.
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
    except Exception:
        pass

    # Determine missing iteration numbers for each algorithm.
    missing_algs = {}
    for alg in expected_algs:
        if alg in skip_list:
            continue
        current_iters = existing_iters.get(alg, set())
        missing_iters = sorted(set(range(1, iterations + 1)) - current_iters)
        if missing_iters:
            missing_algs[alg] = missing_iters

    found_msgs = []
    not_run_msgs = []

    if missing_algs and any(data is not None for data in size_results.values()):
        for alg in missing_algs:
            data = size_results.get(alg)
            # data[4] holds the current iteration count.
            if data is not None:
                if data[4] == 0 or data[4] == iterations:
                    # If no iterations or complete, just print the name.
                    found_msgs.append(alg)
                else:
                    # Otherwise, show partial iteration progress.
                    found_msgs.append(f"{alg} ({data[4]}/{iterations} iterations)")
            else:
                not_run_msgs.append(alg)

        if found_msgs:
            max_items = min(10, len(found_msgs))
            display_msg = ", ".join(found_msgs[:max_items])
            if len(found_msgs) > max_items:
                display_msg += f", and {len(found_msgs) - max_items} more..."
            print(
                f"Found existing results for: {display_msg}; running additional iterations."
            )

        if not_run_msgs:
            max_items = min(10, len(not_run_msgs))
            display_msg = ", ".join(not_run_msgs[:max_items])
            if len(not_run_msgs) > max_items:
                display_msg += f", and {len(not_run_msgs) - max_items} more..."
            print(f"Running results for algorithms that haven't started: {display_msg}")

    if not missing_algs:
        return size_results, skip_list

    completed_counts = {}
    tasks = {}

    # Choose executor based on per_run_timeout setting.
    if per_run_timeout:
        executor_workers = min(num_workers, 2)
        ExecutorClass = ThreadPoolExecutor
    else:
        executor_workers = num_workers
        ExecutorClass = ProcessPoolExecutor

    with ExecutorClass(max_workers=executor_workers) as executor:
        for alg, missing_list in missing_algs.items():
            for iter_num in missing_list:
                if shutdown_requested:
                    print(
                        "Shutdown requested. Exiting update_missing_iterations_concurrent immediately."
                    )
                    sys.exit(0)
                if per_run_timeout:
                    future = executor.submit(
                        safe_run_iteration, get_algorithms()[alg], size, threshold
                    )
                else:
                    future = executor.submit(run_iteration, get_algorithms()[alg], size)
                tasks[future] = (alg, iter_num)

        # Process each future as it completes.
        for future in as_completed(tasks):
            if shutdown_requested:
                for f in tasks:
                    f.cancel()
                print(
                    "Shutdown requested during task processing. Exiting loop without recording DNFs."
                )
                sys.exit(0)
            alg, iter_num = tasks[future]
            completed_counts[alg] = completed_counts.get(alg, 0) + 1
            try:
                t = future.result()
            except Exception as e:
                print(f"{alg} error on size {size} iteration {iter_num}: {e}")
                t = None
            with open(csv_path, "a", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(
                    [alg, size, iter_num, "DNF" if t is None else f"{t:.8f}"]
                )
            if size_results.get(alg) is None:
                size_results[alg] = (None, None, None, None, 0, {})
            old_times = size_results[alg][5]
            old_times[iter_num] = t
            new_count = len(old_times)
            size_results[alg] = (None, None, None, None, new_count, old_times)
            if completed_counts[alg] == len(missing_algs.get(alg, [])):
                # Compute statistics once all missing iterations are complete.
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
                    f"Average for {alg} on size {size}: {format_time(avg, False)} "
                    + (f"(DNF: {dnf_count}/{len(times_list)})" if dnf_count > 0 else "")
                )
    return size_results, skip_list

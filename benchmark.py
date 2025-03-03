"""
This module executes sorting algorithm benchmarks across various array sizes.

It generates CSV files with performance results for each array size, runs multiple iterations
of each sorting algorithm concurrently, and aggregates the results. Detailed markdown reports
are produced—including per-size ranking tables and individual algorithm reports—and the main
README file is rebuilt to reflect overall performance and any skipped algorithms.
"""

import atexit
import csv
import os
import sys
import datetime
import signal
from multiprocessing import Pipe, Process
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

# Import sorting algorithms and helper functions.
from algorithms import *
from utils import compute_median, format_time, run_iteration, compute_average
from csv_utils import get_csv_results_for_size, sort_csv_alphabetically
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown

# Global flag to indicate a shutdown has been requested.
shutdown_requested = False


def signal_handler(signum, frame):
    """
    Signal handler for graceful shutdown.

    This handler is invoked when a SIGINT (Ctrl+C) or SIGTERM is received.
    It sets a global flag that is checked throughout the module to cancel pending tasks and exit.

    Parameters:
        signum (int): The signal number.
        frame (FrameType): The current stack frame.
    """
    global shutdown_requested
    shutdown_requested = True
    print("\nShutdown requested. Cancelling pending tasks and exiting gracefully...")


# Register signal handlers for SIGINT and SIGTERM.
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def on_exit():
    """
    atexit handler to print a final message upon exiting.

    This function is called when the program terminates.
    """
    if shutdown_requested:
        print("Exiting due to shutdown request.")
    else:
        print("Exiting normally.")


atexit.register(on_exit)


def safe_run_target(conn, sort_func, size):
    """
    Run a single iteration of a sorting algorithm and send its result via a connection.

    This function is executed in a separate process. It measures the runtime of a sorting
    algorithm for an array of a given size and sends the elapsed time (or an error) back via the pipe.

    Parameters:
        conn (Connection): A multiprocessing connection to send back the result.
        sort_func (callable): The sorting function to be executed.
        size (int): The size of the array to be sorted.

    Returns:
        None: The result is sent back over the connection.
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

    This function creates a new process to run the sorting algorithm with a given timeout.
    If the process exceeds the timeout, it is terminated and None is returned.

    Parameters:
        sort_func (callable): The sorting function to execute.
        size (int): The size of the array to sort.
        timeout (float): Maximum allowed time (in seconds) for the iteration.

    Returns:
        float or None: The elapsed time if the iteration finishes in time; otherwise, None.
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


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    A geometric progression is used for small sizes, and an exponential (doubling)
    progression is used for larger sizes up to 1 trillion.

    Returns:
        list of int: A sorted list of array sizes.
    """
    n_small = 15
    small_sizes = [
        int(round(5 * ((200 / 3) ** (i / (n_small - 1))))) for i in range(n_small)
    ]
    large_sizes = []
    size = 100
    while size < 1e12:
        large_sizes.append(int(size))
        size *= 2
    large_sizes.append(int(1e12))
    return sorted(set(small_sizes + large_sizes))


def get_num_workers():
    """
    Determine the number of worker processes to use.

    This function selects a fraction of available CPU cores based on the current time.
    At night, more cores are used; during the day, fewer cores are used. Additionally,
    if the SLOW_MODE environment variable is set, the count is further reduced.

    Returns:
        int: The number of worker processes (at least 1).
    """
    total = os.cpu_count() or 1
    now = datetime.datetime.now().time()
    if datetime.time(23, 30) <= now or now <= datetime.time(9, 30):
        workers = max(int(total * 0.75), 1)
    else:
        workers = max(int(total * 0.5), 1)
    if os.environ.get("SLOW_MODE", "").lower() == "true":
        workers = max(int(workers * 0.5), 1)
    return workers


def algorithms():
    """
    Return a mapping of algorithm names to their sorting functions.

    Returns:
        dict: Keys are algorithm names (str) and values are callable sorting functions.
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
        "Counting Sort": counting_sort,
        "Cubesort": cubesort,
        "Cycle Sort": cycle_sort,
        "Exchange Sort": exchange_sort,
        "Flash Sort": flash_sort,
        "Franceschini's Method": franceschinis_method,
        "Gnome Sort": gnome_sort,
        "Heap Sort": heap_sort,
        "Hyper Quick": hyper_quick,
        "I Can't Believe It Can Sort": i_cant_believe_it_can_sort,
        "Insertion Sort": insertion_sort,
        "Intro Sort": intro_sort,
        "Library Sort": library_sort,
        "LSD Radix Sort": lsd_radix_sort,
        "Merge Insertion Sort": merge_insertion_sort,
        "Merge Sort": merge_sort,
        "Merge Sort In-Place": merge_sort_inplace,
        "MSD Radix Sort": msd_radix_sort,
        "MSD Radix Sort In-Place": msd_radix_sort_inplace,
        "Odd-Even Sort": odd_even_sort,
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
    per_run_timeout=False,
):
    """
    Schedule and execute missing iterations for each algorithm concurrently.

    This function reads the existing CSV file to determine which iteration numbers
    (from 1 to iterations) are missing for each algorithm, and schedules tasks to fill
    those gaps. If a shutdown is requested, it immediately raises a KeyboardInterrupt
    to stop further processing.

    Parameters:
        csv_path (str): Path to the CSV file for the current array size.
        size (int): The current array size.
        expected_algs (list): List of algorithm names.
        size_results (dict): In-memory benchmark results for the current size.
        iterations (int): Total iterations desired per algorithm.
        skip_list (dict): Algorithms to be skipped for future sizes.
        threshold (float): Time threshold (in seconds) used for performance checks.
        num_workers (int): Number of worker processes to use.
        per_run_timeout (bool): Whether to enforce a timeout on each iteration.

    Returns:
        tuple: Updated size_results and skip_list.
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

    # Print status messages.
    for alg, missing_list in missing_algs.items():
        if not size_results.get(alg) or size_results[alg][4] == 0:
            print(
                f"{alg} has no iterations yet; scheduling {len(missing_list)} iterations."
            )
        else:
            print(
                f"{alg} needs {len(missing_list)} additional iterations (current count: {size_results[alg][4]})."
            )

    if not missing_algs:
        return size_results, skip_list

    completed_counts = {}  # Track how many missing iterations have been completed.
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
                    raise KeyboardInterrupt
                if per_run_timeout:
                    future = executor.submit(
                        safe_run_iteration, algorithms()[alg], size, threshold
                    )
                else:
                    future = executor.submit(run_iteration, algorithms()[alg], size)
                tasks[future] = (alg, iter_num)

        # Process each future as it completes.
        for future in as_completed(tasks):
            if shutdown_requested:
                for f in tasks:
                    f.cancel()
                print(
                    "Shutdown requested during task processing. Exiting loop without recording DNFs."
                )
                raise KeyboardInterrupt
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
                # Once all missing iterations for an algorithm are completed, compute statistics.
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


def update_overall_results(
    size, size_results, expected_algs, overall_totals, per_alg_results, iterations
):
    """
    Update cumulative benchmark results after processing a given array size.

    For each algorithm, update the overall total time and count, and store the per-algorithm
    performance statistics (average, min, max, median) for the current array size.

    Parameters:
        size (int): The current array size.
        size_results (dict): The computed statistics for each algorithm at this size.
        expected_algs (list): List of algorithm names.
        overall_totals (dict): Aggregated performance totals for each algorithm.
        per_alg_results (dict): Per-algorithm performance records.
        iterations (int): Total iterations executed per algorithm.
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
    Process benchmarking for a single array size.

    This function retrieves (or creates) the CSV file for the given size, fills in any missing iterations,
    updates overall and per-algorithm results, and decides whether to skip an algorithm for future sizes
    based on performance.

    Parameters:
        size (int): The current array size.
        iterations (int): Total iterations desired per algorithm.
        threshold (float): Performance threshold in seconds.
        expected_algs (list): List of algorithm names.
        overall_totals (dict): Aggregated totals for each algorithm.
        per_alg_results (dict): Performance records per algorithm.
        skip_list (dict): Algorithms to be skipped for future sizes.
        per_run_timeout (bool): Whether to enforce a timeout on each iteration.

    Returns:
        tuple: Updated size_results and skip_list.
    """
    csv_path, size_results = get_csv_results_for_size(size, expected_algs)
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
    sort_csv_alphabetically(csv_path)
    _, updated_results = get_csv_results_for_size(size, expected_algs)
    update_overall_results(
        size,
        updated_results,
        expected_algs,
        overall_totals,
        per_alg_results,
        iterations,
    )

    for alg, data in updated_results.items():
        if data is not None and data[4] == iterations and alg not in skip_list:
            successful_times = [x for x in data[5] if x is not None]
            dnf_count = data[4] - len(successful_times)
            if (successful_times and compute_average(successful_times) > threshold) or (
                data[4] > 0 and dnf_count / data[4] >= 0.5
            ):
                skip_list[alg] = size
                print(
                    f"Skipping {alg} for future sizes (avg > threshold or high DNF ratio, skipped at size {size})."
                )
    return size_results, skip_list


def run_sorting_tests(iterations=500, threshold=300, per_run_timeout=False):
    """
    Execute benchmark tests over multiple array sizes and generate reports.

    This is the main driver function. It generates array sizes, initializes overall statistics,
    and iterates through each size to perform benchmarking. It checks for shutdown requests and exits
    immediately if a shutdown is detected.

    Parameters:
        iterations (int): Number of iterations per algorithm per size.
        threshold (float): Time threshold (in seconds) for determining if an algorithm should be skipped.
        per_run_timeout (bool): Whether to enforce a timeout on each iteration.

    Returns:
        None
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
            for alg, data in size_results.items():
                if data is not None and data[0] > threshold and alg not in skip_list:
                    skip_list[alg] = size
            with open(details_path, "a") as f:
                write_markdown(f, size, size_results, skip_list)
            rebuild_readme(overall_totals, details_path, skip_list)
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting gracefully.")
        sys.exit(0)

    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

"""
This module executes sorting algorithm benchmarks across various array sizes.

It generates CSV files with performance results for each array size, runs multiple iterations
of each sorting algorithm concurrently, and aggregates the results. Detailed markdown reports
are produced—including per-size ranking tables and individual algorithm reports—and the main
README file is rebuilt to reflect overall performance and any skipped algorithms.
"""

import csv
import os
import datetime
from multiprocessing import Pipe, Process
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor, as_completed

# Import sorting algorithms and helper functions.
from algorithms import *
from utils import compute_median, format_time, run_iteration, compute_average
from csv_utils import get_csv_results_for_size, sort_csv_alphabetically
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown


def safe_run_target(conn, sort_func, size):
    """
    Execute a single sorting iteration and send the result through a connection.

    This function is run in a separate process to allow enforcing a timeout.

    Parameters:
        conn: Connection object for sending the result.
        sort_func: The sorting function to execute.
        size: The size of the array to sort.
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
    Execute a sorting iteration with a timeout.

    A separate process is spawned to run the sort iteration via safe_run_target.
    If the process does not complete within 'timeout' seconds, it is terminated and
    the iteration is marked as DNF (by returning None).

    Parameters:
        sort_func: The sorting function to run.
        size: The size of the array to sort.
        timeout: Maximum allowed time in seconds for the iteration.

    Returns:
        The elapsed time (float) if the iteration completes in time, or None if it times out.
    """
    parent_conn, child_conn = Pipe()
    p = Process(target=safe_run_target, args=(child_conn, sort_func, size))
    p.start()
    p.join(timeout)
    if p.is_alive():
        p.terminate()
        p.join()
        return None  # Mark iteration as DNF (Did Not Finish)
    if parent_conn.poll():
        res = parent_conn.recv()
        return None if isinstance(res, Exception) else res
    return None


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    Combines a geometric progression for small sizes with an exponential (doubling)
    progression for larger sizes, up to 1 trillion.

    Returns:
        List of unique array sizes.
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
    Determine the number of worker processes based on time of day and environment.

    Uses a higher fraction of cores at night (75%) and a lower fraction during the day (50%).
    If the SLOW_MODE environment variable is set to "true", the worker count is halved.

    Returns:
        Number of workers (at least 1).
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
    Return a dictionary mapping algorithm names to their corresponding sorting functions.

    Returns:
        Dictionary where keys are algorithm names and values are sorting functions.
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
    per_run_timeout=None,
):
    """
    Run missing iterations concurrently for each algorithm and update CSV results.

    For each algorithm that has fewer than 'iterations' completed, this function runs the
    additional iterations concurrently. If a per-run timeout is specified, the iteration is
    canceled if it exceeds the timeout and marked as DNF. Results are written immediately to the CSV.

    Parameters:
        csv_path: Path to the CSV file for the current size.
        size: Current array size.
        expected_algs: List of expected algorithm names.
        size_results: Current in-memory results for the given size.
        iterations: Desired number of iterations per algorithm.
        skip_list: Dict mapping algorithms to the size at which they were skipped.
        threshold: Time threshold in seconds to skip an algorithm.
        num_workers: Number of worker processes available.
        per_run_timeout: Optional timeout (in seconds) for each iteration.

    Returns:
        Updated (size_results, skip_list)
    """
    missing_algs = {}
    found_msgs = []
    # Calculate how many iterations are missing for each algorithm.
    for alg in expected_algs:
        if alg in skip_list:
            continue
        data = size_results[alg]
        if data is None:
            missing_algs[alg] = iterations
        else:
            count = data[4]
            if count < iterations:
                missing_algs[alg] = iterations - count
                found_msgs.append(f"{alg} ({count})" if count > 0 else f"{alg}")

    if missing_algs and any(data is not None for data in size_results.values()):
        if found_msgs:
            max_items = min(10, len(found_msgs))
            display_msg = ", ".join(found_msgs[:max_items])
            if len(found_msgs) > max_items:
                display_msg += f", and {len(found_msgs) - max_items} more..."
            print(
                f"Found existing results for: {display_msg}; running additional iterations."
            )
        else:
            missing_keys = list(missing_algs.keys())
            max_items = min(10, len(missing_keys))
            display_msg = ", ".join(missing_keys[:max_items])
            if len(missing_keys) > max_items:
                display_msg += f", and {len(missing_keys) - max_items} more..."
            print(f"Missing iterations for: {display_msg}")
    if not missing_algs:
        return size_results, skip_list

    completed_counts = {}
    tasks = {}

    # If a timeout is active, reduce concurrency to limit resource usage.
    if per_run_timeout is not None:
        executor_workers = min(num_workers, 2)
        ExecutorClass = ThreadPoolExecutor
    else:
        executor_workers = num_workers
        ExecutorClass = ProcessPoolExecutor

    with ExecutorClass(max_workers=executor_workers) as executor:
        for alg, missing in missing_algs.items():
            start_iter = (
                (size_results[alg][4] + 1) if size_results[alg] is not None else 1
            )
            for i in range(missing):
                if per_run_timeout is not None:
                    future = executor.submit(
                        safe_run_iteration, algorithms()[alg], size, per_run_timeout
                    )
                else:
                    future = executor.submit(run_iteration, algorithms()[alg], size)
                tasks[future] = (alg, start_iter + i)

        for future in as_completed(tasks):
            alg, iter_index = tasks[future]
            completed_counts[alg] = completed_counts.get(alg, 0) + 1
            try:
                t = future.result()
            except Exception as e:
                print(f"{alg} error on size {size} iteration {iter_index}: {e}")
                t = None
            with open(csv_path, "a", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(
                    [alg, size, iter_index, "DNF" if t is None else f"{t:.8f}"]
                )
            if size_results[alg] is None:
                size_results[alg] = (None, None, None, None, 0, [])
            old_count = size_results[alg][4]
            old_times = size_results[alg][5]
            size_results[alg] = (None, None, None, None, old_count + 1, old_times + [t])
            if completed_counts[alg] == missing_algs[alg]:
                times = size_results[alg][5]
                successful_times = [x for x in times if x is not None]
                dnf_count = len(times) - len(successful_times)
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
                size_results[alg] = (avg, min_time, max_time, median, len(times), times)
                print(
                    f"Average for {alg} on size {size}: {format_time(avg, False)} (DNF: {dnf_count}/{len(times)})"
                )
                if (
                    avg > threshold
                    or (len(times) > 0 and dnf_count / len(times) >= 0.5)
                ) and alg not in skip_list:
                    skip_list[alg] = size
                    print(
                        f"Skipping {alg} for future sizes (avg > threshold or high DNF ratio, skipped at size {size})."
                    )
    return size_results, skip_list


def update_overall_results(
    size, size_results, expected_algs, overall_totals, per_alg_results, iterations
):
    """
    Update aggregated totals and per-algorithm records for the given array size.

    For each algorithm, the overall sum and count are updated based on the average
    result at the current size, and a record is appended.

    Parameters:
        size: Current array size.
        size_results: Results for the current size.
        expected_algs: List of algorithm names.
        overall_totals: Dict mapping algorithm names to aggregated totals.
        per_alg_results: Dict mapping algorithm names to their performance records.
        iterations: Number of iterations per algorithm for this size.
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
    per_run_timeout=None,
):
    """
    Process benchmark tests for a single array size.

    Retrieves or creates the CSV file for the current size, runs missing iterations concurrently,
    sorts the CSV file, and updates aggregated results.

    Parameters:
        size: Array size to test.
        iterations: Desired iterations per algorithm.
        threshold: Runtime threshold for skipping an algorithm.
        expected_algs: List of expected algorithm names.
        overall_totals: Aggregated totals dictionary.
        per_alg_results: Per-algorithm performance records.
        skip_list: Dict mapping algorithms to the size at which they were skipped.
        per_run_timeout: Optional timeout (in seconds) for each iteration.

    Returns:
        Updated (size_results, skip_list).
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
    return size_results, skip_list


def run_sorting_tests(iterations=500, threshold=300, per_run_timeout=None):
    """
    Run benchmarks across multiple array sizes and generate reports.

    The process includes:
      1. Generating a list of array sizes.
      2. Initializing overall totals and per-algorithm records.
      3. For each array size:
         a. Running missing iterations concurrently.
         b. Writing a per-size markdown report.
         c. Rebuilding the main README.
      4. Generating individual algorithm reports.

    Parameters:
        iterations: Iterations per algorithm per size.
        threshold: Runtime threshold (seconds) for skipping an algorithm.
        per_run_timeout: Optional per-iteration timeout in seconds.
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
        previous_skip = set(skip_list.keys())
        for alg, data in size_results.items():
            if data is not None and data[0] > threshold and alg not in skip_list:
                skip_list[alg] = size
        new_skipped = {
            alg: skip_list[alg] for alg in skip_list if alg not in previous_skip
        }
        with open(details_path, "a") as f:
            write_markdown(f, size, size_results, removed=list(new_skipped.keys()))
        rebuild_readme(overall_totals, details_path, skip_list)

    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

"""
This module executes sorting algorithm benchmarks across various array sizes.

It generates CSV files with performance results for each array size, runs multiple iterations
of each sorting algorithm concurrently, and aggregates the results. Detailed markdown reports
are produced, including per-size ranking tables and individual algorithm reports, and the main
README file is rebuilt to reflect overall performance and any skipped algorithms.
"""

import csv
import os
import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

# Import sorting algorithms and helper functions.
from algorithms import *
from utils import compute_median, format_time, run_iteration, compute_average
from csv_utils import get_csv_results_for_size, sort_csv_alphabetically
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    This function creates two progressions:
    - A geometric progression for small array sizes.
    - An exponential (doubling) progression for large array sizes (up to 1 trillion).

    Returns:
        list: Sorted list of unique array sizes.
    """
    n_small = 15
    # Calculate small sizes using a geometric progression.
    small_sizes = [
        int(round(5 * ((200 / 3) ** (i / (n_small - 1))))) for i in range(n_small)
    ]
    large_sizes = []
    size = 100
    # Generate large sizes by doubling until reaching 1 trillion.
    while size < 1e12:
        large_sizes.append(int(size))
        size *= 2
    large_sizes.append(int(1e12))
    sizes = sorted(set(small_sizes + large_sizes))
    return sizes


def get_num_workers():
    """
    Determine the number of worker processes based on the current time of day and environment.

    The number of workers is chosen as follows:
    - Between 11:30 PM and 9:30 AM: 75% of available CPU cores.
    - Otherwise: 50% of available CPU cores.
    If the SLOW_MODE environment variable is set to "true", the worker count is halved.

    Returns:
        int: The number of worker processes to use (at least 1).
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
    Provide a dictionary mapping algorithm names to their corresponding sorting functions.

    Returns:
        dict: Mapping from algorithm name (str) to its sorting function.
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
):
    """
    Identify missing iterations for each algorithm and run them concurrently.

    This function creates a single ProcessPoolExecutor for all missing iterations across
    all algorithms. It submits all missing iteration tasks concurrently and processes each
    as soon as it completes. As each iteration's result is returned, it is immediately written
    to the CSV and used to update the in-memory results. When all iterations for an algorithm
    are complete, its performance statistics are recalculated and printed.

    Additionally, if there are already some results in memory, the function prints a notification
    detailing which algorithms already have some iterations completed.

    Parameters:
        csv_path (str): Path to the CSV file for the current array size.
        size (int): The current array size being benchmarked.
        expected_algs (list): List of expected algorithm names.
        size_results (dict): Existing results for each algorithm (mapping algorithm to tuple).
        iterations (int): Desired number of iterations per algorithm.
        skip_list (dict): Mapping of algorithm names to the size at which they were skipped.
        threshold (float): Runtime threshold in seconds; algorithms exceeding this average are skipped.
        num_workers (int): Number of worker processes to use for concurrent execution.

    Returns:
        tuple: Updated size_results and skip_list.
    """
    missing_algs = {}
    found_msgs = []
    # Determine how many additional iterations each algorithm needs.
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
                found_msgs.append(f"{alg} ({count})")

    if missing_algs and any(data is not None for data in size_results.values()):
        if found_msgs:
            max_items = min(10, len(found_msgs))
            if len(found_msgs) > max_items:
                display_msg = (
                    ", ".join(found_msgs[:max_items])
                    + f", and {len(found_msgs) - max_items} more..."
                )
            else:
                display_msg = ", ".join(found_msgs)
            print(
                f"Found existing results for: {display_msg}; running additional iterations."
            )
        else:
            missing_keys = list(missing_algs.keys())
            max_items = min(10, len(missing_keys))
            if len(missing_keys) > max_items:
                display_msg = (
                    ", ".join(missing_keys[:max_items])
                    + f", and {len(missing_keys) - max_items} more..."
                )
            else:
                display_msg = ", ".join(missing_keys)
            print(f"Missing iterations for: {display_msg}")

    if not missing_algs:
        return size_results, skip_list

    # Dictionary to track the number of completed iterations per algorithm.
    completed_counts = {}

    # Dictionary mapping each future to its (algorithm, iteration index).
    tasks = {}

    # Submit all missing iteration tasks concurrently across all algorithms.
    with ProcessPoolExecutor(max_workers=num_workers) as executor:
        for alg, missing in missing_algs.items():
            start_iter = (
                (size_results[alg][4] + 1) if size_results[alg] is not None else 1
            )
            for i in range(missing):
                future = executor.submit(run_iteration, algorithms()[alg], size)
                tasks[future] = (alg, start_iter + i)

        # Process each task as soon as it completes.
        for future in as_completed(tasks):
            alg, iter_index = tasks[future]
            if alg not in completed_counts:
                completed_counts[alg] = 0
            try:
                t = future.result()
                # Append the result to the CSV file.
                with open(csv_path, "a", newline="") as csv_file:
                    writer = csv.writer(csv_file)
                    writer.writerow([alg, size, iter_index, f"{t:.8f}"])
                # Update the in-memory results for this algorithm.
                if size_results[alg] is None:
                    size_results[alg] = (None, None, None, None, 0, [])
                old_count = size_results[alg][4]
                old_times = size_results[alg][5]
                size_results[alg] = (
                    None,  # Average (to be recalculated)
                    None,  # Min (to be recalculated)
                    None,  # Max (to be recalculated)
                    None,  # Median (to be recalculated)
                    old_count + 1,
                    old_times + [t],
                )
            except Exception as e:
                print(f"{alg} error on size {size} iteration {iter_index}: {e}")
            # Increment the count for this algorithm.
            completed_counts[alg] += 1
            # Once all iterations for an algorithm are complete, recalculate its stats.
            if completed_counts[alg] == missing_algs[alg]:
                times = size_results[alg][5]
                avg = compute_average(times)
                median = compute_median(times)
                size_results[alg] = (
                    avg,
                    min(times),
                    max(times),
                    median,
                    len(times),
                    times,
                )
                print(f"Average for {alg} on size {size}: {format_time(avg, False)}")
                if avg > threshold and alg not in skip_list:
                    skip_list[alg] = size
                    print(
                        f"Skipping {alg} for future sizes (average > 5min, skipped at size {size})."
                    )
    return size_results, skip_list


def update_overall_results(
    size, size_results, expected_algs, overall_totals, per_alg_results, iterations
):
    """
    Update the aggregated overall totals and per-algorithm results for a given array size.

    For each algorithm that produced results, this function updates the cumulative total time,
    iteration count, and appends a record (array size, average, min, max, median) to the per-algorithm results.

    Parameters:
        size (int): The current array size.
        size_results (dict): Mapping {algorithm: (avg, min, max, median, count, times)} for the current size.
        expected_algs (list): List of expected algorithm names.
        overall_totals (dict): Aggregated totals for each algorithm (with keys "sum" and "count").
        per_alg_results (dict): Per-algorithm performance records.
        iterations (int): Number of iterations per algorithm for the current size.
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
):
    """
    Process benchmark tests for a specific array size.

    This function performs the following steps:
    1. Retrieves or creates the CSV file for the given size.
    2. Determines the current number of worker processes.
    3. Runs missing iterations concurrently for each algorithm.
    4. Sorts the CSV file alphabetically.
    5. Re-reads the updated CSV to recalculate overall statistics.
    6. Updates aggregated totals and per-algorithm records.

    Parameters:
        size (int): The array size to test.
        iterations (int): Desired iterations per algorithm.
        threshold (float): Runtime threshold for skipping an algorithm.
        expected_algs (list): List of expected algorithm names.
        overall_totals (dict): Aggregated performance totals for each algorithm.
        per_alg_results (dict): Per-algorithm performance records.
        skip_list (dict): Mapping of algorithm names to the size at which they were skipped.

    Returns:
        tuple: Updated size_results and skip_list.
    """
    csv_path, size_results = get_csv_results_for_size(size, expected_algs)
    current_workers = get_num_workers()
    # Update worker count if it has changed.
    process_size.workers = getattr(process_size, "workers", None)
    if process_size.workers is None or current_workers != process_size.workers:
        if process_size.workers is None:
            print(
                f"Using {current_workers} worker{'s' if current_workers > 1 else ''}."
            )
        else:
            print(
                f"Changing workers from {process_size.workers} worker{'s' if process_size.workers > 1 else ''} to {current_workers} worker{'s' if current_workers > 1 else ''}."
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
    )
    # Sort the CSV file alphabetically.
    sort_csv_alphabetically(csv_path)

    # Re-read the CSV file to get updated results.
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


def run_sorting_tests(iterations=500, threshold=300):
    """
    Run sorting algorithm benchmarks across various array sizes and generate reports.

    This function orchestrates the complete benchmarking process:
    1. Generates a list of array sizes to test.
    2. Initializes overall totals and per-algorithm performance records.
    3. For each array size:
       a. Processes the benchmark tests.
       b. Writes per-size markdown details.
       c. Rebuilds the main README with updated rankings.
    4. Generates individual markdown reports for each algorithm.
    5. Prints a completion message.

    Parameters:
        iterations (int, optional): Number of iterations per algorithm per array size. Default is 250.
        threshold (float, optional): Runtime threshold (in seconds) for skipping an algorithm. Default is 300 seconds.
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

    # Determine and print the initial worker count before processing any sizes.
    initial_workers = get_num_workers()
    print(f"Using {initial_workers} worker{'s' if initial_workers > 1 else ''}.")
    process_size.workers = initial_workers

    # Process each array size.
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
        )

        # Determine newly skipped algorithms for this size.
        previous_skip = set(skip_list.keys())
        for alg, data in size_results.items():
            if data is not None and data[0] > threshold and alg not in skip_list:
                skip_list[alg] = size
        new_skipped = {
            alg: skip_list[alg] for alg in skip_list if alg not in previous_skip
        }

        # Append per-size markdown ranking table with notes for any newly skipped algorithms.
        with open(details_path, "a") as f:
            write_markdown(f, size, size_results, removed=list(new_skipped.keys()))

        # Rebuild the main README with updated overall totals and skip list.
        rebuild_readme(overall_totals, details_path, skip_list)

    # Generate individual markdown files for each algorithm.
    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

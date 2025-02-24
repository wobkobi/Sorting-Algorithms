"""
benchmark.py

This module implements the core logic for executing sorting benchmarks across multiple array sizes.
It handles:
  - Generating array sizes.
  - Reading and writing CSV files using csv_utils.py.
  - Running benchmark iterations in parallel.
  - Aggregating and updating overall statistics.
  - Generating markdown reports (per-size ranking tables and individual algorithm reports).

If an algorithm's CSV data for a given size does not contain the desired number of iterations,
the missing iterations are computed and appended. The CSV is then sorted alphabetically.
A helper ensures that new data is appended on a new line if the process stops and restarts.
"""

import csv
import os
from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor, as_completed

# Import sorting algorithms.
from algorithms import *

# Import helper functions from utils.
from utils import (
    compute_median,
    format_time,
    run_iteration,
    compute_average,
)

# Import CSV utilities.
from csv_utils import (
    read_csv_results,
    ensure_csv_ends_with_newline,
    sort_csv_alphabetically,
)

# Import markdown report functions.
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    Produces two progressions:
      - A geometric progression for small sizes (from 3 to 100 over 15 steps).
      - An exponential progression (doubling) for larger sizes (starting at 100 up to 1 trillion).

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
    # Calculate large sizes by doubling until reaching 1 trillion.
    while size < 1e12:
        large_sizes.append(int(size))
        size *= 2
    large_sizes.append(int(1e12))
    return sorted(set(small_sizes + large_sizes))


def algorithms():
    """
    Provide a dictionary mapping algorithm names to their corresponding sorting functions.

    Returns:
        dict: Mapping {algorithm_name: sorting_function, ...}
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
        "Cycle Sort": cycle_sort,
        "Exchange Sort": exchange_sort,
        "External Merge Sort": external_merge_sort,
        "Flash Sort": flash_sort,
        "Franceschini's Method": franceschinis_method,
        "Gnome Sort": gnome_sort,
        "Heap Sort": heap_sort,
        "Hyper Quick": hyper_quick,
        "I Can't Believe It Can Sort": i_cant_believe_it_can_sort,
        "Insertion Sort": insertion_sort,
        "Intro Sort": intro_sort,
        "Library Sort": library_sort,
        "Merge Insertion Sort": merge_insertion_sort,
        "Merge Sort": merge_sort,
        "MSD Radix Sort": msd_radix_sort,
        "MSD Radix Sort In-Place": msd_radix_sort_inplace,
        "Odd-Even Sort": odd_even_sort,
        "P-Merge Sort": p_merge_sort,
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


def run_sorting_tests(iterations=250, threshold=300):
    """
    Execute sorting benchmarks across various array sizes and compile the results.

    Parameters:
        iterations (int): Number of iterations per algorithm per array size (default: 250).
        threshold (int): Threshold in seconds for average runtime; algorithms exceeding this are skipped (default: 300).

    For each array size:
      1. If a CSV file exists, read its contents using read_csv_results (from csv_utils.py) and check
         whether each expected algorithm has the desired number of iterations.
         If an algorithm has fewer iterations, determine how many are missing.
      2. If the CSV file is new, create it and write the header row.
      3. For each algorithm with missing iterations (or missing entirely), run the additional iterations
         and append the new rows to the CSV.
      4. Ensure the CSV ends with a newline, then sort it alphabetically by the algorithm name.
      5. Update overall aggregated statistics and per-algorithm records.
      6. Append a per-size markdown ranking table (with a note for any algorithms removed at that size) to a details file.
      7. Rebuild the main README.md file to display overall top-20 rankings and the list of skipped algorithms.

    Algorithms with an average runtime exceeding the threshold are skipped in future sizes.
    """
    sizes = generate_sizes()
    expected_algs = list(algorithms().keys())

    overall_totals = {alg: {"sum": 0, "count": 0} for alg in expected_algs}
    per_alg_results = {alg: [] for alg in expected_algs}
    skip_list = set()

    # Get the initial number of worker processes.
    num_workers = max((os.cpu_count() or 1) // 2, 1)
    print(
        f"Using {num_workers} worker{'s' if num_workers > 1 else ''} for parallel execution."
    )

    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)

    details_path = "details.md"
    with open(details_path, "w") as f:
        f.write("")

    # Process each array size.
    for size in sizes:
        print(f"\nTesting array size: {size}")
        csv_filename = f"results_{size}.csv"
        csv_path = os.path.join(output_folder, csv_filename)

        csv_exists = os.path.exists(csv_path)
        if csv_exists:
            print(f"CSV file for size {size} exists; reading results.")
            size_results = read_csv_results(csv_path, expected_algs)
        else:
            # Create a new CSV file and write the header row.
            with open(csv_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(
                    ["Algorithm", "Array Size", "Iteration", "Elapsed Time (seconds)"]
                )
            size_results = OrderedDict((alg, None) for alg in expected_algs)

        # Ensure the CSV file ends with a newline.
        ensure_csv_ends_with_newline(csv_path)

        # Identify missing iterations for each algorithm.
        missing_algs = {}
        found_msgs = []
        for alg in expected_algs:
            if alg in skip_list:
                continue
            data = size_results[alg]
            if data is None:
                missing_algs[alg] = iterations
            else:
                count = data[4]  # Number of iterations recorded.
                if count < iterations:
                    missing_algs[alg] = iterations - count
                    found_msgs.append(f"{alg} ({count} iterations)")
        if csv_exists and missing_algs:
            if found_msgs:
                print(
                    f"Found existing results for: {', '.join(found_msgs)}; running additional iterations."
                )
            else:
                print(f"Missing iterations for: {', '.join(missing_algs.keys())}")

        # Run additional iterations for each algorithm that is missing iterations.
        if missing_algs:
            with open(csv_path, "a", newline="") as csv_file:
                writer = csv.writer(csv_file)
                for alg_name, additional in missing_algs.items():
                    sort_func = algorithms()[alg_name]
                    new_times = []
                    with ProcessPoolExecutor(max_workers=num_workers) as executor:
                        futures = [
                            executor.submit(run_iteration, sort_func, size)
                            for _ in range(additional)
                        ]
                        # Determine starting iteration number.
                        start_iter = (
                            size_results[alg_name][4] + 1
                            if size_results[alg_name] is not None
                            else 1
                        )
                        for i, future in enumerate(
                            as_completed(futures), start=start_iter
                        ):
                            try:
                                t = future.result()
                                new_times.append(t)
                                writer.writerow([alg_name, size, i, f"{t:.8f}"])
                                csv_file.flush()
                            except Exception as e:
                                print(
                                    f"{alg_name} error on size {size} iteration {i}: {e}"
                                )
                                new_times = []
                                break
                    if new_times:
                        if size_results[alg_name] is None:
                            combined = new_times
                        else:
                            combined = size_results[alg_name][5] + new_times
                        avg = compute_average(combined)
                        median = compute_median(combined)
                        size_results[alg_name] = (
                            avg,
                            min(combined),
                            max(combined),
                            median,
                            len(combined),
                            combined,
                        )
                        print(
                            f"Average for {alg_name} on size {size}: {format_time(avg)}"
                        )
                        if avg > threshold and alg_name not in skip_list:
                            skip_list.add(alg_name)
                            print(
                                f"Skipping {alg_name} for future sizes (average > 5min)."
                            )
                    else:
                        size_results[alg_name] = None
            print(f"Updated CSV for size {size}.")

        # Sort the CSV file alphabetically by algorithm name.
        sort_csv_alphabetically(csv_path)

        # Update overall totals and per-algorithm results.
        for alg in expected_algs:
            data = size_results[alg]
            if data is not None:
                overall_totals[alg]["sum"] += data[0] * iterations
                overall_totals[alg]["count"] += iterations
                per_alg_results[alg].append((size, data[0], data[1], data[2], data[3]))

        # Determine newly skipped algorithms for this size.
        previous_skip = set(skip_list)
        for alg, data in size_results.items():
            if data is not None and data[0] > threshold:
                skip_list.add(alg)
        new_skipped = skip_list - previous_skip

        # Append the per-size markdown ranking table with a note for any algorithms removed.
        with open(details_path, "a") as f:
            write_markdown(f, size, size_results, removed=list(new_skipped))

        # Rebuild the main README with updated overall totals and the skip list.
        rebuild_readme(overall_totals, details_path, skip_list)

    # Generate individual markdown files for each algorithm.
    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

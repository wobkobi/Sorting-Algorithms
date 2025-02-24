"""
benchmark.py

This module contains the main logic for executing sorting benchmarks across
various array sizes. It handles reading/writing CSV files, executing benchmarks
in parallel, aggregating results, and generating markdown reports.
"""

import csv
import os
import math
import time
import psutil
from collections import OrderedDict
from concurrent.futures import ProcessPoolExecutor, as_completed

# Import all sorting functions from the algorithms package.
from algorithms import *

# Import helper functions from utils and markdown utilities.
from utils import compute_median, format_time, run_iteration, compute_average
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    This function creates two distinct progressions:
      - A geometric progression for small sizes (from 3 to 100, distributed over 15 steps).
      - An exponential progression (doubling) for larger sizes, starting at 100 and increasing up to 1 trillion.

    Returns:
        list: A sorted list of unique integer array sizes.
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


def read_csv_results(csv_path, expected_algs):
    """
    Read benchmark results from a CSV file for a specific array size and compute statistics.

    The CSV file is expected to have a header and rows formatted as:
      [Algorithm, Array Size, Iteration, Elapsed Time (seconds)]

    For each expected algorithm (as provided in expected_algs), this function computes:
      - Average elapsed time.
      - Minimum elapsed time.
      - Maximum elapsed time.
      - Median elapsed time.

    If an algorithm is missing from the CSV, its result is set to None.
    The results are returned in the order specified by expected_algs.

    Parameters:
        csv_path (str): Path to the CSV file.
        expected_algs (list): List of expected algorithm names.

    Returns:
        OrderedDict: Mapping {algorithm: (avg, min, max, median)} (or None if missing),
                     maintaining the order of expected_algs.
    """
    algorithm_times = {}
    with open(csv_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip the header row
        for row in reader:
            alg = row[0]
            try:
                t = float(row[3])
            except Exception:
                continue
            algorithm_times.setdefault(alg, []).append(t)

    results = OrderedDict()
    for alg in expected_algs:
        if alg in algorithm_times and algorithm_times[alg]:
            times = algorithm_times[alg]
            avg = compute_average(times)
            median = compute_median(times)
            results[alg] = (avg, min(times), max(times), median)
        else:
            results[alg] = None
    return results


def algorithms():
    """
    Provide a mapping from algorithm names to their corresponding sorting functions.

    This mapping is used to iterate through the available sorting algorithms.

    Returns:
        dict: Dictionary mapping algorithm names (str) to their sorting function objects.
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


def run_sorting_tests():
    """
    Execute sorting benchmarks across various array sizes and compile results.

    For each array size:
      - If a CSV file with previous results exists, read it and verify that every expected algorithm is present.
      - For any missing algorithm (i.e. not present in the CSV), run 250 iterations and append the new results to the CSV.
      - Update overall totals and per-algorithm results based on the new data.
      - Append a per-size ranking table to a details markdown file, including a note for any algorithms removed at that size.
      - Rebuild the main README.md file to display overall top-10 rankings and the list of skipped algorithms.

    Algorithms with an average runtime exceeding 5 minutes are skipped in future sizes.
    """
    sizes = generate_sizes()
    iterations = 250
    threshold = 300  # 5 minutes cutoff (in seconds)

    expected_algs = list(algorithms().keys())

    overall_totals = {alg: {"sum": 0, "count": 0} for alg in expected_algs}
    per_alg_results = {alg: [] for alg in expected_algs}
    skip_list = set()

    # Determine initial worker count.
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
            # For a new CSV, initialize an ordered dictionary with all expected algorithms set to None.
            size_results = OrderedDict((alg, None) for alg in expected_algs)

        # Identify missing algorithms that need to be benchmarked (and not already skipped).
        missing_algs = [
            alg
            for alg in expected_algs
            if size_results[alg] is None and alg not in skip_list
        ]

        # Only print missing message if the CSV already existed.
        if csv_exists and missing_algs:
            print(f"Missing results for: {', '.join(missing_algs)}")

        # For each missing algorithm, run benchmarks and append the results to the CSV.
        if missing_algs:
            with open(csv_path, "a", newline="") as csv_file:
                writer = csv.writer(csv_file)
                for alg_name in missing_algs:
                    sort_func = algorithms()[alg_name]
                    times = []
                    with ProcessPoolExecutor(max_workers=num_workers) as executor:
                        futures = [
                            executor.submit(run_iteration, sort_func, size)
                            for _ in range(iterations)
                        ]
                        for i, future in enumerate(as_completed(futures), start=1):
                            try:
                                t = future.result()
                                times.append(t)
                                writer.writerow([alg_name, size, i, f"{t:.8f}"])
                                csv_file.flush()
                            except Exception as e:
                                print(
                                    f"{alg_name} error on size {size} iteration {i}: {e}"
                                )
                                times = []
                                break
                    if times:
                        avg = compute_average(times)
                        result = (avg, min(times), max(times), compute_median(times))
                        size_results[alg_name] = result
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

        # Update overall totals and per-algorithm results (in expected order).
        for alg in expected_algs:
            data = size_results[alg]
            if data is not None:
                overall_totals[alg]["sum"] += data[0] * iterations
                overall_totals[alg]["count"] += iterations
                per_alg_results[alg].append((size, data[0], data[1], data[2], data[3]))

        # Determine newly skipped algorithms at this size.
        previous_skip = set(skip_list)
        for alg, data in size_results.items():
            if data is not None and data[0] > threshold:
                skip_list.add(alg)
        new_skipped = skip_list - previous_skip

        # Append per-size markdown ranking table with note for removed algorithms.
        with open(details_path, "a") as f:
            write_markdown(f, size, size_results, removed=list(new_skipped))

        # Rebuild the main README with updated overall totals and skipped algorithms.
        rebuild_readme(overall_totals, details_path, skip_list)

    # Generate individual markdown files for each algorithm.
    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

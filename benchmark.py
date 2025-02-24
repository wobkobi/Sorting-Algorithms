import csv
import os
import math
import time
import psutil
from concurrent.futures import ProcessPoolExecutor, as_completed

# Import all sorting functions from the algorithms package.
from algorithms import *

# Import helper functions.
from utils import compute_median, format_time, run_iteration, compute_average
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    Creates two progressions:
      - A geometric progression for small sizes (3 to 100, over 15 steps).
      - An exponential progression (doubling) for larger sizes, starting at 100 up to 1 trillion.

    Returns:
        list: Sorted list of unique integer array sizes.
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


def read_csv_results(csv_path):
    """
    Read benchmark results from a CSV file for a specific array size and compute statistics.

    The CSV file is expected to have a header and rows in the format:
      [Algorithm, Array Size, Iteration, Elapsed Time (seconds)]

    For each algorithm, calculates:
      - Average elapsed time.
      - Minimum elapsed time.
      - Maximum elapsed time.
      - Median elapsed time.

    Parameters:
        csv_path (str): Path to the CSV file.

    Returns:
        dict: Mapping {algorithm: (avg, min, max, median)}.
    """
    algorithm_times = {}
    with open(csv_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header
        for row in reader:
            alg = row[0]
            try:
                t = float(row[3])
            except Exception:
                continue
            algorithm_times.setdefault(alg, []).append(t)

    results = {}
    for alg, times in algorithm_times.items():
        avg = compute_average(times)
        median = compute_median(times)
        if avg is not None:
            results[alg] = (avg, min(times), max(times), median)
    return results


def algorithms():
    """
    Provide a mapping from algorithm names to their corresponding sorting functions.

    Returns:
        dict: {algorithm_name: sort_function, ...}
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


def get_num_workers():
    """
    Determine the number of worker processes to use, targeting a usage of at most 70%
    of the CPU cores, and reducing that number further if overall CPU usage is high.

    The calculation uses the formula:
        available = total_cores * 0.7 * (1 - (current_cpu_usage / 100))

    This ensures that if the system is idle (0% usage), up to 70% of the cores are used.
    If the CPU usage increases, the number of worker processes decreases accordingly.

    Returns:
        int: The number of worker processes to use (at least 1).
    """
    total = os.cpu_count() or 1
    current_usage = psutil.cpu_percent(interval=0.1)
    available = total * 0.7 * (1 - (current_usage / 100.0))
    return max(math.floor(available), 1)


def run_sorting_tests():
    """
    Execute sorting benchmarks over various array sizes and compile results.

    For each size:
      - If a CSV with previous results exists, read it; otherwise, run 250 iterations per algorithm.
      - Write results to CSV and update overall totals and per-algorithm data.
      - Append a per-size ranking table to a details markdown file; if any algorithms are removed
        due to performance issues, pass the list to the markdown writer.
      - Rebuild README.md with overall top-10 rankings and list of skipped algorithms.
      - Generate individual markdown files for each algorithm at the end.

    Algorithms exceeding a 5-minute average runtime are skipped in future sizes.
    """
    sizes = generate_sizes()
    iterations = 250
    threshold = 300  # 5 minutes cutoff (in seconds)

    # Data structures to hold aggregated results.
    overall_totals = {alg: {"sum": 0, "count": 0} for alg in algorithms().keys()}
    per_alg_results = {alg: [] for alg in algorithms().keys()}
    skip_list = set()

    # Initial worker count for parallel execution.
    num_workers = max((os.cpu_count() or 1) // 2, 1)
    print(
        f"Using {num_workers} worker{'s' if num_workers > 1 else ''} for parallel execution."
    )

    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)

    details_path = "details.md"
    with open(details_path, "w") as f:
        f.write("")

    # Iterate over each generated array size.
    for size in sizes:
        print(f"\nTesting array size: {size}")
        csv_filename = f"results_{size}.csv"
        csv_path = os.path.join(output_folder, csv_filename)
        size_results = {}

        # Read existing CSV data if available.
        if os.path.exists(csv_path):
            print(f"CSV file for size {size} exists; reading results.")
            size_results = read_csv_results(csv_path)
        else:
            # Otherwise, run benchmarks and write CSV.
            with open(csv_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(
                    ["Algorithm", "Array Size", "Iteration", "Elapsed Time (seconds)"]
                )
                # Process each algorithm.
                for alg_name, sort_func in algorithms().items():
                    if alg_name in skip_list:
                        size_results[alg_name] = None
                        continue

                    times = []
                    # Use a fixed number of workers for this run.
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
                        # Record average, min, max, and median times.
                        size_results[alg_name] = (
                            avg,
                            min(times),
                            max(times),
                            compute_median(times),
                        )
                        print(
                            f"Average for {alg_name} on size {size}: {format_time(avg)}"
                        )
                        if avg > threshold and alg_name not in skip_list:
                            skip_list.add(alg_name)
                            print(
                                f"Skipping {alg_name} for future sizes (current average > 5min)."
                            )
                    else:
                        size_results[alg_name] = None
            print(f"Ran tests for size {size} and saved CSV.")

        # Update aggregated results.
        for alg, data in size_results.items():
            if data is not None:
                overall_totals[alg]["sum"] += data[0] * iterations
                overall_totals[alg]["count"] += iterations
                # Append results: (size, average, min, max, median)
                per_alg_results[alg].append((size, data[0], data[1], data[2], data[3]))

        # Determine newly skipped algorithms at this size.
        previous_skip = set(skip_list)
        for alg, data in size_results.items():
            if data is not None:
                current_avg = data[0]
                if current_avg > threshold and alg not in skip_list:
                    skip_list.add(alg)
                    print(f"Skipping {alg} for future sizes (current average > 5min).")
        new_skipped = skip_list - previous_skip

        with open(details_path, "a") as f:
            write_markdown(f, size, size_results, removed=list(new_skipped))

        # Rebuild the main README with updated rankings and skipped algorithms.
        rebuild_readme(overall_totals, details_path, skip_list)

    # Write individual markdown files for each algorithm.
    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

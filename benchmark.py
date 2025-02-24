import csv
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

# Import all sorting functions from the algorithms package.
from algorithms import *

# Import helper functions.
from utils import compute_median, format_time, run_iteration, compute_average
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    This function creates two progressions of sizes:
      - A geometric progression for small sizes ranging from 3 to 100, distributed over 15 steps.
      - An exponential progression (doubling) for larger sizes, starting from 100 and going up to 1 trillion.

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


def read_csv_results(csv_path):
    """
    Read a CSV file containing benchmark results for a specific array size and compute statistics.

    The CSV file is expected to have a header and rows containing:
      [Algorithm, Array Size, Iteration, Elapsed Time (seconds)]
    For each algorithm, this function computes:
      - Average elapsed time.
      - Minimum elapsed time.
      - Maximum elapsed time.
      - Median elapsed time.

    Parameters:
        csv_path (str): The file path to the CSV file containing benchmark data.

    Returns:
        dict: A mapping from algorithm names to a tuple of computed statistics:
              (average time, minimum time, maximum time, median time).
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

    This mapping is used to iterate through the available sorting algorithms during benchmarking.

    Returns:
        dict: A dictionary where keys are algorithm names (str) and values are the sorting function objects.
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
    Execute a series of sorting benchmarks across various array sizes and compile the results.

    The process for each array size includes:
      - Checking if a CSV file with previous benchmark results exists; if so, reading from it.
      - If no CSV exists, running 250 iterations per algorithm (in parallel) to gather benchmark data,
        writing the results to a CSV file.
      - Updating overall totals and per-algorithm results for later reporting.
      - Appending a per-size ranking table to a details markdown file.
      - Rebuilding the main README.md file with an overall top 10 ranking and a list of skipped algorithms.
      - Immediately printing each algorithm's average time after completing its iterations, and
        skipping algorithms (for future sizes) if their average exceeds a 5-minute threshold.

    After all sizes are processed, individual markdown files for each algorithm are generated under
    "results/algorithms" (if they don't already exist).

    This function ties together the CSV reading/writing, parallel execution, and markdown reporting.
    """
    sizes = generate_sizes()
    iterations = 250
    threshold = 300  # 5 minutes per iteration cutoff in seconds

    # Initialize overall totals and per-algorithm results for aggregation.
    overall_totals = {alg: {"sum": 0, "count": 0} for alg in algorithms().keys()}
    per_alg_results = {alg: [] for alg in algorithms().keys()}
    skip_list = set()

    num_workers = max((os.cpu_count() or 1) // 2, 1)
    print(
        f"Using {num_workers} worker{'s' if num_workers > 1 else ''} for parallel execution."
    )

    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)

    details_path = "details.md"
    with open(details_path, "w") as f:
        f.write("")

    # Iterate over all generated array sizes.
    for size in sizes:
        print(f"\nTesting array size: {size}")
        csv_filename = f"results_{size}.csv"
        csv_path = os.path.join(output_folder, csv_filename)
        size_results = {}

        # If CSV results already exist for this size, load them.
        if os.path.exists(csv_path):
            print(f"CSV file for size {size} exists; reading results.")
            size_results = read_csv_results(csv_path)
        else:
            # Otherwise, run benchmark tests and write results to CSV.
            with open(csv_path, "w", newline="") as csv_file:
                writer = csv.writer(csv_file)
                writer.writerow(
                    ["Algorithm", "Array Size", "Iteration", "Elapsed Time (seconds)"]
                )
                for alg_name, sort_func in algorithms().items():
                    if alg_name in skip_list:
                        size_results[alg_name] = None
                        continue

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
                        # Record the average, minimum, and maximum times.
                        size_results[alg_name] = (avg, min(times), max(times))
                        # Print the average time immediately.
                        print(
                            f"Average for {alg_name} on size {size}: {format_time(avg)}"
                        )
                        # If the average exceeds the threshold, mark the algorithm to be skipped in future sizes.
                        if avg > threshold and alg_name not in skip_list:
                            skip_list.add(alg_name)
                            print(
                                f"Skipping {alg_name} for future sizes (current average > 5min)."
                            )
                    else:
                        size_results[alg_name] = None
            print(f"Ran tests for size {size} and saved CSV.")

        # Update overall totals and record per-algorithm results for the current size.
        for alg, data in size_results.items():
            if data is not None:
                overall_totals[alg]["sum"] += data[0] * iterations
                overall_totals[alg]["count"] += iterations
                per_alg_results[alg].append((size, data[0], data[1], data[2]))

        # Insert a markdown comment in the details file if new algorithms are being skipped at this size.
        previous_skip = set(skip_list)
        for alg, data in size_results.items():
            if data is not None:
                current_avg = data[0]
                # (The average is already printed above for each algorithm.)
                if current_avg > threshold and alg not in skip_list:
                    skip_list.add(alg)
                    print(f"Skipping {alg} for future sizes (current average > 5min).")
        new_skipped = skip_list - previous_skip
        if new_skipped:
            with open(details_path, "a") as f:
                f.write(
                    f"<!-- At size {size}, the following algorithms were removed: {', '.join(sorted(new_skipped))} -->\n\n"
                )

        # Append the per-size markdown ranking table.
        with open(details_path, "a") as f:
            write_markdown(f, size, size_results)

        # Rebuild the main README with updated overall and skipped algorithms information.
        rebuild_readme(overall_totals, details_path, skip_list)

    # After processing all sizes, write individual markdown files for each algorithm.
    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

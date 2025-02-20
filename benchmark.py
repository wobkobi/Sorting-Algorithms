import csv
import os
import random
import time
import math
from concurrent.futures import ProcessPoolExecutor, as_completed

# Import sorting functions from the "algorithms" folder.
from algorithms.bead_sort import bead_sort
from algorithms.bitonic_sort import bitonic_sort_parallel
from algorithms.block_sort import block_sort
from algorithms.bogo_sort import bogo_sort
from algorithms.bubble_sort import bubble_sort
from algorithms.bucket_sort import bucket_sort
from algorithms.burst_sort import burst_sort
from algorithms.cocktail_sort import cocktail_sort
from algorithms.comb_sort import comb_sort
from algorithms.cycle_sort import cycle_sort
from algorithms.external_merge_sort import external_merge_sort
from algorithms.flash_sort import flash_sort
from algorithms.gnome_sort import gnome_sort
from algorithms.heap_sort import heap_sort
from algorithms.hyper_quick import hyper_quick
from algorithms.insertion_sort import insertion_sort
from algorithms.intro_sort import intro_sort
from algorithms.merge_sort import merge_sort
from algorithms.odd_even_sort import odd_even_sort
from algorithms.pancake_sort import pancake_sort
from algorithms.patience_sort import patience_sort
from algorithms.pigeonhole_sort import pigeonhole_sort
from algorithms.polyphase_merge_sort import polyphase_merge_sort
from algorithms.postman_sort import postman_sort
from algorithms.quick_sort import quick_sort
from algorithms.radix_sort import radix_sort
from algorithms.replacement_selection_sort import replacement_selection_sort
from algorithms.sample_sort import sample_sort
from algorithms.selection_sort import selection_sort
from algorithms.shell_sort import shell_sort
from algorithms.sleep_sort import sleep_sort
from algorithms.smooth_sort import smooth_sort
from algorithms.spaghetti_sort import spaghetti_sort
from algorithms.stooge_sort import stooge_sort
from algorithms.strand_sort import strand_sort
from algorithms.tim_sort import tim_sort
from algorithms.tournament_sort import tournament_sort
from algorithms.tree_sort import tree_sort

# Import helper functions from utils.py and markdown_utils.py.
from utils import format_time, group_rankings, run_iteration
from markdown_utils import write_markdown, write_algorithm_markdown


def generate_sizes():
    """
    Generate logarithmically spaced sizes by combining:
      - 20 small sizes between 5 and 1000.
      - 10 large sizes between 1000 and 100,000,000.

    Returns:
        Sorted list of unique sizes.
    """
    small_sizes = [int(round(5 * (1000 / 5) ** (i / 19))) for i in range(20)]
    big_sizes = [int(round(1000 * (100000000 / 1000) ** (i / 9))) for i in range(10)]
    return sorted(list(set(small_sizes + big_sizes)))


def read_csv_results(csv_path):
    """
    Read the CSV file for a given array size and compute the average, minimum, and maximum times for each algorithm.

    Parameters:
        csv_path (str): The path to the CSV file.

    Returns:
        dict: Mapping from algorithm name to a tuple (avg, min, max).
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
        if times:
            avg_time = sum(times) / len(times)
            results[alg] = (avg_time, min(times), max(times))
    return results


def algorithms():
    """
    Return a dictionary mapping algorithm names to their corresponding sort functions.

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
        "External Merge Sort": external_merge_sort,
        "Flash Sort": flash_sort,
        "Gnome Sort": gnome_sort,
        "Heap Sort": heap_sort,
        "Hyper Quick": hyper_quick,
        "Insertion Sort": insertion_sort,
        "Intro Sort": intro_sort,
        "Merge Sort": merge_sort,
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
        "Smooth Sort": smooth_sort,
        "Spaghetti Sort": spaghetti_sort,
        "Stooge Sort": stooge_sort,
        "Strand Sort": strand_sort,
        "Tim Sort": tim_sort,
        "Tournament Sort": tournament_sort,
        "Tree Sort": tree_sort,
    }


def rebuild_readme(overall_totals, details_path, skip_list):
    """
    Rebuild the main README.md file using the per-size details from details.md and overall averages.

    The README.md will start with an Overall Top 10 table (with hyperlinks to individual algorithm Markdown files)
    and a "Skipped Algorithms" section listing those algorithms that are being skipped due to an overall average
    exceeding 30 minutes, followed by the per-size ranking sections.

    Parameters:
        overall_totals (dict): Mapping from algorithm to a dict with keys "sum" and "count".
        details_path (str): Path to the details markdown file.
        skip_list (set): Set of algorithm names that have been skipped.
    """
    overall = {}
    for alg, totals in overall_totals.items():
        if totals["count"] > 0:
            overall[alg] = totals["sum"] / totals["count"]
    overall_ranking = sorted(overall.items(), key=lambda x: x[1])

    overall_lines = []
    overall_lines.append("# Sorting Algorithms Benchmark Results\n\n")
    overall_lines.append(
        "## Overall Top 10 Algorithms (by average time across sizes)\n"
    )
    overall_lines.append("| Rank | Algorithm | Overall Average Time |\n")
    overall_lines.append("| ---- | --------- | -------------------- |\n")
    for rank, (alg, avg_time) in enumerate(overall_ranking[:10], start=1):
        link = f"[{alg}](results/algorithms/{alg.replace(' ', '_')}.md)"
        overall_lines.append(f"| {rank} | {link} | {format_time(avg_time)} |\n")
    overall_lines.append("\n")

    if skip_list:
        overall_lines.append("## Skipped Algorithms\n")
        overall_lines.append(
            "The following algorithms were skipped for subsequent sizes because their overall average exceeded 30 minutes:\n\n"
        )
        overall_lines.append(", ".join(sorted(skip_list)) + "\n\n")

    with open(details_path, "r") as f:
        details_content = f.read()

    with open("README.md", "w") as md_file:
        md_file.writelines(overall_lines)
        md_file.write(details_content)
        md_file.flush()


def run_sorting_tests():
    """
    Execute the sorting benchmarks over logarithmically generated array sizes.

    For each size:
      - If a CSV file exists in the 'results' folder, read its contents; otherwise, perform 250 iterations
        for each algorithm in parallel (writing each iteration’s result immediately to the CSV file).
      - Update overall totals and accumulate per-algorithm results.
      - Append the per-size ranking table (showing average times only) to a details file on disk.
      - Rebuild the main README.md file after each size so that the Overall Top 10 table (with hyperlinks)
        and a "Skipped Algorithms" section appear at the top.
      - Dynamically add any algorithm to the skip list if its overall average (from all available data)
        exceeds 30 minutes (1800 seconds). Also, print a message when an algorithm is skipped.

    After processing all sizes:
      - Write separate Markdown files for each algorithm (if they don't already exist) in "results/algorithms",
        showing array size, average time, minimum time, and maximum time.
    """
    sizes = generate_sizes()
    iterations = 250

    # 15 minutes threshold in seconds.
    threshold_seconds = 15 * 60

    # Initialize dynamic skip list.
    skip_list = set()

    # Use half of available CPU cores.
    num_workers = max((os.cpu_count() or 2) // 2, 1)
    print(f"Using {num_workers} worker(s) for parallel execution.")

    overall_totals = {alg: {"sum": 0, "count": 0} for alg in algorithms().keys()}
    per_alg_results = {
        alg: [] for alg in algorithms().keys()
    }  # For per-algorithm Markdown.

    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)

    # Create (or clear) a details file to store per-size markdown sections.
    details_path = "details.md"
    with open(details_path, "w") as details_file:
        details_file.write("")

    # Process each size.
    for size in sizes:
        print(f"\nTesting array size: {size}")
        csv_filename = f"results_{size}.csv"
        csv_path = os.path.join(output_folder, csv_filename)
        size_results = {}  # Mapping: algorithm -> (avg, min, max)

        # If CSV exists, read its contents; otherwise, run tests.
        if os.path.exists(csv_path):
            print(f"CSV file for size {size} exists; reading results.")
            size_results = read_csv_results(csv_path)
        else:
            with open(csv_path, "w", newline="") as csv_file:
                csv_writer = csv.writer(csv_file)
                csv_writer.writerow(
                    ["Algorithm", "Array Size", "Iteration", "Elapsed Time (seconds)"]
                )
                for alg_name, sort_func in algorithms().items():
                    # Skip if algorithm is already in the dynamic skip list.
                    if alg_name in skip_list:
                        size_results[alg_name] = None
                        continue

                    times_list = []
                    with ProcessPoolExecutor(max_workers=num_workers) as executor:
                        futures = [
                            executor.submit(run_iteration, sort_func, size)
                            for _ in range(iterations)
                        ]
                        for i, future in enumerate(as_completed(futures), start=1):
                            try:
                                elapsed_time = future.result()
                                times_list.append(elapsed_time)
                                # Write CSV row immediately after each iteration.
                                csv_writer.writerow(
                                    [alg_name, size, i, f"{elapsed_time:.8f}"]
                                )
                                csv_file.flush()
                            except Exception as e:
                                print(
                                    f"{alg_name} error on size {size} iteration {i}: {e}"
                                )
                                times_list = []
                                break
                    if times_list:
                        avg_time = sum(times_list) / len(times_list)
                        min_time = min(times_list)
                        max_time = max(times_list)
                        size_results[alg_name] = (avg_time, min_time, max_time)
                    else:
                        size_results[alg_name] = None
            print(f"Ran tests for size {size} and saved CSV.")

        # Update overall totals and accumulate per-algorithm results.
        for alg, data in size_results.items():
            if data is not None:
                overall_totals[alg]["sum"] += data[0]
                overall_totals[alg]["count"] += 1
                per_alg_results[alg].append((size, data[0], data[1], data[2]))

        # Dynamically update the skip list based on overall averages (from all available data).
        for alg, totals in overall_totals.items():
            if totals["count"] > 0:
                overall_avg = totals["sum"] / totals["count"]
                if overall_avg > threshold_seconds and alg not in skip_list:
                    skip_list.add(alg)
                    print(f"Skipping {alg} for future sizes (overall average > 30min).")

        # Append per-size markdown (average times only) to details.md.
        from markdown_utils import write_markdown

        with open(details_path, "a") as details_file:
            write_markdown(details_file, size, size_results)

        # Rebuild the main README.md file after each size.
        rebuild_readme(overall_totals, details_path, skip_list)

    # Write per-algorithm Markdown files (only if they don't already exist).
    from markdown_utils import write_algorithm_markdown

    write_algorithm_markdown(per_alg_results)
    print(
        "\nCSV files saved in 'results' folder, README.md updated in the root, and per-algorithm Markdown files written in 'results/algorithms'."
    )


def rebuild_readme(overall_totals, details_path, skip_list):
    """
    Rebuild the main README.md file using the per-size details from details.md and overall averages.

    The README.md will start with an Overall Top 10 table (with hyperlinks to individual algorithm Markdown files)
    and a "Skipped Algorithms" section, followed by the per-size ranking sections from details.md.

    Parameters:
        overall_totals (dict): Mapping from algorithm to a dict with keys "sum" and "count".
        details_path (str): Path to the details markdown file.
        skip_list (set): Set of algorithm names that are being skipped.
    """
    overall = {}
    for alg, totals in overall_totals.items():
        if totals["count"] > 0:
            overall[alg] = totals["sum"] / totals["count"]
    overall_ranking = sorted(overall.items(), key=lambda x: x[1])

    overall_lines = []
    overall_lines.append("# Sorting Algorithms Benchmark Results\n\n")
    overall_lines.append(
        "## Overall Top 10 Algorithms (by average time across sizes)\n"
    )
    overall_lines.append("| Rank | Algorithm | Overall Average Time |\n")
    overall_lines.append("| ---- | --------- | -------------------- |\n")
    for rank, (alg, avg_time) in enumerate(overall_ranking[:10], start=1):
        link = f"[{alg}](results/algorithms/{alg.replace(' ', '_')}.md)"
        overall_lines.append(f"| {rank} | {link} | {format_time(avg_time)} |\n")
    overall_lines.append("\n")

    if skip_list:
        overall_lines.append("## Skipped Algorithms\n")
        overall_lines.append(
            "The following algorithms have been skipped for subsequent sizes because their overall average exceeded 30 minutes:\n\n"
        )
        overall_lines.append(", ".join(sorted(skip_list)) + "\n\n")

    with open(details_path, "r") as f:
        details_content = f.read()

    with open("README.md", "w") as md_file:
        md_file.writelines(overall_lines)
        md_file.write(details_content)
        md_file.flush()


if __name__ == "__main__":
    run_sorting_tests()

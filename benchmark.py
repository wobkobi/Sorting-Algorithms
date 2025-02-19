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
    Generate logarithmically spaced sizes by combining 20 small sizes (5 to 1000)
    and 10 large sizes (1000 to 100,000,000).

    Returns:
        Sorted list of unique sizes.
    """
    small_sizes = [int(round(5 * (1000 / 5) ** (i / 19))) for i in range(20)]
    big_sizes = [int(round(1000 * (100000000 / 1000) ** (i / 9))) for i in range(10)]
    return sorted(list(set(small_sizes + big_sizes)))


def read_csv_results(csv_path):
    """
    Read the CSV file for a given size and compute average, min, and max times for each algorithm.

    Parameters:
        csv_path (str): Path to the CSV file.

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
    Return a dictionary mapping algorithm names to their sort function.
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


def run_sorting_tests():
    """
    Run sorting benchmarks for logarithmically generated sizes.

    - Generates sizes by combining 20 small sizes (5 to 1000) and 10 large sizes (1000 to 100,000,000).
    - Each algorithm is run for a fixed number of iterations (500) in parallel.
    - Inefficient algorithms are skipped beyond their defined thresholds.
    - For each size, if a CSV file exists, results are read from it; otherwise, tests are executed and CSV is created.
    - Updates the main Markdown file ("README.md") in the root with grouped per-size rankings (average, min, max).
    - Also writes separate Markdown files per algorithm in "results/algorithms" if they do not already exist.
    - Computes overall averages and appends an overall Top 10 table.
    """
    sizes = generate_sizes()
    iterations = 500

    # Skip thresholds for very inefficient algorithms.
    skip_thresholds = {
        "Bogo Sort": 15,
        "Sleep Sort": 20,
        "Stooge Sort": 20,
        "Spaghetti Sort": 20,
        "Strand Sort": 20,
        "Bead Sort": 40,
    }

    # Use half of available cores.
    num_workers = max((os.cpu_count() or 2) // 2, 1)
    print(f"Using {num_workers} worker(s) for parallel execution.")

    overall_totals = {alg: {"sum": 0, "count": 0} for alg in algorithms().keys()}
    per_alg_results = {
        alg: [] for alg in algorithms().keys()
    }  # For per-algorithm Markdown.

    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)

    md_path = "README.md"
    with open(md_path, "w") as md_file:
        md_file.write("# Sorting Algorithms Benchmark Results\n")
        md_file.write(
            "This document is updated as tests run. It contains per-size rankings of each sorting algorithm.\n\n"
        )

        for size in sizes:
            print(f"\nTesting array size: {size}")
            csv_filename = f"results_{size}.csv"
            csv_path = os.path.join(output_folder, csv_filename)
            size_results = {}  # Mapping: algorithm -> (avg, min, max)

            # If CSV exists, read results; otherwise, run tests.
            if os.path.exists(csv_path):
                print(f"CSV file for size {size} exists; reading results.")
                size_results = read_csv_results(csv_path)
            else:
                with open(csv_path, "w", newline="") as csv_file:
                    csv_writer = csv.writer(csv_file)
                    csv_writer.writerow(
                        [
                            "Algorithm",
                            "Array Size",
                            "Iteration",
                            "Elapsed Time (seconds)",
                        ]
                    )
                    for alg_name, sort_func in algorithms().items():
                        if (
                            alg_name in skip_thresholds
                            and size > skip_thresholds[alg_name]
                        ):
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
                                    csv_writer.writerow(
                                        [alg_name, size, i, f"{elapsed_time:.8f}"]
                                    )
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

            # Update overall totals and per-algorithm results.
            for alg, data in size_results.items():
                if data is not None:
                    overall_totals[alg]["sum"] += data[0]
                    overall_totals[alg]["count"] += 1
                    per_alg_results[alg].append((size, data[0], data[1], data[2]))

            # Write per-size ranking to the main Markdown file.
            write_markdown(md_file, size, size_results)

        # Compute overall averages.
        overall = {}
        for alg, totals in overall_totals.items():
            if totals["count"] > 0:
                overall[alg] = totals["sum"] / totals["count"]
        overall_ranking = sorted(overall.items(), key=lambda x: x[1])
        md_file.write("## Overall Top 10 Algorithms (by average time across sizes)\n")
        md_file.write("| Rank | Algorithm | Overall Average Time |\n")
        md_file.write("| ---- | --------- | -------------------- |\n")
        for rank, (alg, avg_time) in enumerate(overall_ranking[:10], start=1):
            md_file.write(f"| {rank} | {alg} | {format_time(avg_time)} |\n")
        md_file.write("\n")
        md_file.flush()

    # Write per-algorithm Markdown files (only if they don't already exist).
    write_algorithm_markdown(per_alg_results)
    print(
        "\nCSV files saved in 'results' folder, README.md updated in the root, and per-algorithm markdown files written in 'results/algorithms'."
    )


if __name__ == "__main__":
    run_sorting_tests()

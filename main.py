import csv
import os
import random
import time
import math
from concurrent.futures import ProcessPoolExecutor, as_completed

# Import sorting functions from files within the "algorithms" folder.
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


def format_time(seconds):
    """
    Format elapsed time into a human-readable string (without microseconds detail),
    rounding values to full numbers.

    - If time is less than 1 millisecond, returns "less than 1 millisecond".
    - For times less than 1 second, displays milliseconds (rounded to a whole number).
    - For times between 1 and 60 seconds, displays seconds and milliseconds (both as integers).
    - For times between 60 seconds and 1 hour, displays minutes, seconds, and milliseconds.
    - For times >= 1 hour, displays hours, minutes, and seconds.
    """
    if seconds < 1e-3:
        return "less than 1 millisecond"
    elif seconds < 1:
        ms = int(round(seconds * 1000))
        return f"{ms} millisecond{'s' if ms != 1 else ''}"
    elif seconds < 60:
        sec_int = int(seconds)
        ms = int(round((seconds - sec_int) * 1000))
        return f"{sec_int} second{'s' if sec_int != 1 else ''} and {ms} millisecond{'s' if ms != 1 else ''}"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        rem = seconds % 60
        sec_int = int(rem)
        ms = int(round((rem - sec_int) * 1000))
        return f"{minutes} minute{'s' if minutes != 1 else ''}, {sec_int} second{'s' if sec_int != 1 else ''} and {ms} millisecond{'s' if ms != 1 else ''}"
    else:
        hours = int(seconds // 3600)
        rem = seconds % 3600
        minutes = int(rem // 60)
        sec_int = int(rem % 60)
        return f"{hours} hour{'s' if hours != 1 else ''}, {minutes} minute{'s' if minutes != 1 else ''} and {sec_int} second{'s' if sec_int != 1 else ''}"


def group_rankings(ranking, margin=1e-3):
    """
    Group rankings if consecutive average times are within the margin (default 1 millisecond).
    'ranking' is a sorted list of tuples (algorithm, avg_time).
    Returns a list of groups, where each group is a list of (algorithm, avg_time) tuples.
    """
    groups = []
    if not ranking:
        return groups
    current_group = [ranking[0]]
    for item in ranking[1:]:
        if item[1] - current_group[-1][1] < margin:
            current_group.append(item)
        else:
            groups.append(current_group)
            current_group = [item]
    groups.append(current_group)
    return groups


def run_iteration(sort_func, size):
    """
    Run a single iteration of sort for the given sort function and size.
    Returns the elapsed time in seconds.
    """
    arr = [random.randint(-1000000, 1000000) for _ in range(size)]
    arr_copy = arr.copy()
    start_time = time.perf_counter()
    sort_func(arr_copy)
    return time.perf_counter() - start_time


def run_sorting_tests():
    # Generate sizes logarithmically.
    small_sizes = [int(round(5 * (1000 / 5) ** (i / 19))) for i in range(20)]
    big_sizes = [int(round(1000 * (100000000 / 1000) ** (i / 9))) for i in range(10)]
    sizes = sorted(list(set(small_sizes + big_sizes)))

    iterations = 500  # Run each test 500 times

    # Use the specified skip thresholds.
    skip_thresholds = {
        "Bogo Sort": 15,
        "Sleep Sort": 20,
        "Stooge Sort": 20,
        "Spaghetti Sort": 20,
        "Strand Sort": 20,
        "Bead Sort": 40,
    }

    # Use half of the available cores (as requested).
    num_workers = max((os.cpu_count() or 2) // 2, 1)
    print(f"Using {num_workers} worker(s) for parallel execution.")

    # Ensure output folder exists for CSV files.
    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)

    # Open Markdown file for writing per-size rankings in the root directory.
    md_path = "README.md"
    md_file = open(md_path, "w")
    md_file.write("# Sorting Algorithms Benchmark Results\n")
    md_file.write(
        "This document is updated as tests run. It contains per-size rankings of each sorting algorithm.\n\n"
    )

    # Prepare overall totals for each algorithm.
    algorithms = {
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
    overall_totals = {alg: {"sum": 0, "count": 0} for alg in algorithms.keys()}

    # Process each size.
    for size in sizes:
        print(f"\nTesting array size: {size}")
        # Open a new CSV file for this size.
        csv_filename = f"results_{size}.csv"
        csv_path = os.path.join(output_folder, csv_filename)
        csv_file = open(csv_path, "w", newline="")
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(
            ["Algorithm", "Array Size", "Iteration", "Elapsed Time (seconds)"]
        )

        size_results = {}  # Temporary results for this size.
        for alg_name, sort_func in algorithms.items():
            # Skip inefficient algorithms based on threshold.
            if alg_name in skip_thresholds and size > skip_thresholds[alg_name]:
                size_results[alg_name] = None
                continue

            total_time = 0
            # Use ProcessPoolExecutor to parallelize iterations.
            with ProcessPoolExecutor(max_workers=num_workers) as executor:
                futures = [
                    executor.submit(run_iteration, sort_func, size)
                    for _ in range(iterations)
                ]
                for i, future in enumerate(as_completed(futures), start=1):
                    try:
                        elapsed_time = future.result()
                        total_time += elapsed_time
                        csv_writer.writerow([alg_name, size, i, f"{elapsed_time:.8f}"])
                        csv_file.flush()
                    except Exception as e:
                        print(f"{alg_name} error on size {size} iteration {i}: {e}")
                        total_time = None
                        break

            if total_time is not None:
                avg_time = total_time / iterations
                size_results[alg_name] = avg_time
                overall_totals[alg_name]["sum"] += avg_time
                overall_totals[alg_name]["count"] += 1
                print(f"{alg_name} averaged {format_time(avg_time)} for size {size}.")
            else:
                size_results[alg_name] = None
        csv_file.close()  # Close CSV file for this size.

        # Write per-size ranking to the Markdown file.
        md_file.write(f"## Array Size: {size}\n")
        ranking = [(alg, t) for alg, t in size_results.items() if t is not None]
        if ranking:
            if all(t < 1e-3 for _, t in ranking):
                md_file.write(
                    "All algorithms ran in less than 1 millisecond on this array size; detailed ranking differences are negligible.\n\n"
                )
            else:
                ranking.sort(key=lambda x: x[1])
                groups = group_rankings(ranking, margin=1e-3)
                current_rank = 1
                md_file.write("| Rank | Algorithm(s) | Average Time |\n")
                md_file.write("| ---- | ------------ | ------------ |\n")
                for group in groups:
                    start_rank = current_rank
                    end_rank = current_rank + len(group) - 1
                    rep_time = group[0][1]
                    algs_in_group = ", ".join(alg for alg, _ in group)
                    rank_str = (
                        f"{start_rank}"
                        if start_rank == end_rank
                        else f"{start_rank}-{end_rank}"
                    )
                    md_file.write(
                        f"| {rank_str} | {algs_in_group} | {format_time(rep_time)} |\n"
                    )
                    current_rank = end_rank + 1
                md_file.write("\n")
        else:
            md_file.write("No algorithms produced a result for this array size.\n\n")
        md_file.flush()

    # After processing all sizes, compute overall averages.
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

    md_file.close()
    print(
        "\nCSV files (split by array size) saved in 'results' folder and README.md file updated in the root directory."
    )


if __name__ == "__main__":
    run_sorting_tests()

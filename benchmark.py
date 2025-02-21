import csv
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

# Import sorting functions.
from algorithms import *

# Import helper functions.
from utils import format_time, run_iteration, compute_average
from markdown_utils import write_markdown, write_algorithm_markdown


def generate_sizes():
    """
    Generate logarithmically spaced array sizes.

    Returns:
        list: Sorted list of unique sizes.
    """
    small_sizes = [int(round(5 * (1000 / 5) ** (i / 19))) for i in range(20)]
    big_sizes = [int(round(1000 * (100000000 / 1000) ** (i / 9))) for i in range(10)]
    return sorted(list(set(small_sizes + big_sizes)))


def read_csv_results(csv_path):
    """
    Read CSV file for an array size and compute average, min, and max times per algorithm.

    Parameters:
        csv_path (str): Path to the CSV file.

    Returns:
        dict: Mapping {algorithm: (avg, min, max)}.
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
        avg_time = compute_average(times)
        if avg_time is not None:
            results[alg] = (avg_time, min(times), max(times))
    return results


def algorithms():
    """
    Return mapping of algorithm names to their sorting functions.

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
    Rebuild the main README.md using overall averages and per-size details.

    The README.md includes an Overall Top 10 table (with links to per-algorithm files)
    and a Skipped Algorithms section listing those algorithms removed from future sizes
    because their overall average exceeded 15 minutes.

    Parameters:
        overall_totals (dict): Mapping {algorithm: {"sum": total_time, "count": total_iterations}}.
        details_path (str): Path to the details markdown file.
        skip_list (set): Set of algorithms being skipped.
    """
    overall = {}
    for alg, totals in overall_totals.items():
        if totals["count"] > 0:
            overall[alg] = totals["sum"] / totals["count"]
    overall_ranking = sorted(overall.items(), key=lambda x: x[1])

    lines = []
    lines.append("# Sorting Algorithms Benchmark Results\n\n")
    lines.append("## Overall Top 10 Algorithms (by average time across sizes)\n")
    lines.append("| Rank | Algorithm | Overall Average Time |\n")
    lines.append("| ---- | --------- | -------------------- |\n")
    for rank, (alg, avg_time) in enumerate(overall_ranking[:10], start=1):
        link = f"[{alg}](results/algorithms/{alg.replace(' ', '_')}.md)"
        lines.append(f"| {rank} | {link} | {format_time(avg_time)} |\n")
    lines.append("\n")

    if skip_list:
        lines.append("## Skipped Algorithms\n")
        lines.append(
            "The following algorithms have been removed from future sizes because their average on a given size exceeded 15 minutes:\n\n"
        )
        lines.append(", ".join(sorted(skip_list)) + "\n\n")
        print("Skipped Algorithms:", ", ".join(sorted(skip_list)))
    else:
        lines.append("## Skipped Algorithms\n")
        lines.append("No algorithms were skipped.\n\n")
        print("No algorithms were skipped.")

    with open(details_path, "r") as f:
        details_content = f.read()

    with open("README.md", "w") as md_file:
        md_file.writelines(lines)
        md_file.write(details_content)
        md_file.flush()


def run_sorting_tests():
    """
    Run sorting benchmarks over logarithmically generated array sizes.

    For each size:
      - If a CSV exists for that size, read it; otherwise, perform 250 iterations per algorithm in parallel.
      - Update overall totals and per-algorithm results.
      - Append a per-size ranking table (averages only) to a details file.
      - Rebuild README.md with an Overall Top 10 table and a Skipped Algorithms section.
      - For each algorithm, use the current size's average to decide if it should be added to the skip list.
        (The current size's results are written before the algorithm is skipped for future sizes.)
        When skipping, print a message.

    After all sizes:
      - Write per-algorithm Markdown files in "results/algorithms" (if not already present).
    """
    sizes = generate_sizes()
    iterations = 250
    threshold = 900  # 15 minutes in seconds

    # overall_totals stores the total elapsed time and total iteration count across sizes.
    overall_totals = {alg: {"sum": 0, "count": 0} for alg in algorithms().keys()}
    per_alg_results = {alg: [] for alg in algorithms().keys()}
    skip_list = set()

    # Use 75% of available CPU cores.
    num_workers = max((os.cpu_count() * 3) // 4, 1)
    print(f"Using {num_workers} worker(s) for parallel execution.")

    output_folder = "results"
    os.makedirs(output_folder, exist_ok=True)

    details_path = "details.md"
    with open(details_path, "w") as f:
        f.write("")

    for size in sizes:
        print(f"\nTesting array size: {size}")
        csv_filename = f"results_{size}.csv"
        csv_path = os.path.join(output_folder, csv_filename)
        size_results = {}

        if os.path.exists(csv_path):
            print(f"CSV file for size {size} exists; reading results.")
            size_results = read_csv_results(csv_path)
        else:
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
                        size_results[alg_name] = (avg, min(times), max(times))
                    else:
                        size_results[alg_name] = None
            print(f"Ran tests for size {size} and saved CSV.")

        # Update overall totals and per-algorithm results for the current size.
        for alg, data in size_results.items():
            if data is not None:
                overall_totals[alg]["sum"] += data[0] * iterations
                overall_totals[alg]["count"] += iterations
                per_alg_results[alg].append((size, data[0], data[1], data[2]))

        # Use current size averages to update the skip list.
        for alg, data in size_results.items():
            if data is not None:
                current_avg = data[0]
                print(
                    f"Average for {alg} on size {size}: {format_time(current_avg)} seconds"
                )
                if current_avg > threshold and alg not in skip_list:
                    skip_list.add(alg)
                    print(f"Skipping {alg} for future sizes (current average > 15min).")

        # Append the current size's markdown (all current results are written).

        with open(details_path, "a") as f:
            write_markdown(f, size, size_results)

        rebuild_readme(overall_totals, details_path, skip_list)

    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )


if __name__ == "__main__":
    print("Please run main.py instead. But fine, I'll do it anyway.")
    run_sorting_tests()

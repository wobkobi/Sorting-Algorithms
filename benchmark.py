import csv
import os
from concurrent.futures import ProcessPoolExecutor, as_completed

# Import all sorting functions from the algorithms package.
from algorithms import *

# Import helper functions.
from utils import format_time, run_iteration, compute_average
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown


def generate_sizes():
    """
    Dynamically generate array sizes.

    - For small sizes, generate a geometric progression from 3 to 100 over 15 steps.
    - For larger sizes, use an exponential progression (doubling) from 100 up to 1 trillion.

    Returns:
        list: Sorted list of unique sizes.
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
        avg = compute_average(times)
        if avg is not None:
            results[alg] = (avg, min(times), max(times))
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
    Run sorting benchmarks over dynamically generated array sizes.

    For each size:
      - If a CSV exists for that size, read it; otherwise, perform 250 iterations per algorithm in parallel.
      - Update overall totals and per-algorithm results.
      - Append a per-size ranking table (averages only) to a details file.
      - Rebuild README.md with an Overall Top 10 table and a Skipped Algorithms section.
      - For each algorithm, immediately after its 250 runs are completed, print:
            print(f"Average for {alg} on size {size}: {format_time(current_avg)}")
        and use the current size's average to decide if it should be skipped for future sizes.
        When skipping, print a message and insert a markdown comment indicating which algorithms were removed at that size.

    After processing all sizes:
      - Write per-algorithm Markdown files in "results/algorithms" (if not already present).
    """
    sizes = generate_sizes()
    iterations = 250
    threshold = 300  # 5 minutes per iteration cutoff

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
                        # Immediately print average after finishing 250 iterations.
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

        # Update overall totals and per-algorithm results for the current size.
        for alg, data in size_results.items():
            if data is not None:
                overall_totals[alg]["sum"] += data[0] * iterations
                overall_totals[alg]["count"] += iterations
                per_alg_results[alg].append((size, data[0], data[1], data[2]))

        # Insert markdown comment if new algorithms were skipped at this size.
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

        with open(details_path, "a") as f:
            write_markdown(f, size, size_results)

        rebuild_readme(overall_totals, details_path, skip_list)

    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

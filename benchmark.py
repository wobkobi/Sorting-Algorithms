import gc
import csv
import os
import datetime
from concurrent.futures import ProcessPoolExecutor, as_completed

# Imports remain the same...
from algorithms import *
from utils import compute_median, format_time, run_iteration, compute_average
from csv_utils import get_csv_results_for_size, sort_csv_alphabetically
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown

BATCH_SIZE = 100


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.
    """
    n_small = 15
    # Calculate small sizes using a geometric progression.
    small_sizes = [
        int(round(5 * ((200 / 3) ** (i / (n_small - 1))))) for i in range(n_small)
    ]
    large_sizes = []
    size = 100
    # Double the size until reaching 1 trillion.
    while size < 1e12:
        large_sizes.append(int(size))
        size *= 2
    large_sizes.append(int(1e12))
    sizes = sorted(set(small_sizes + large_sizes))
    print(f"Sizes: {sizes}")
    # Clear temporary lists.
    del small_sizes, large_sizes
    return sizes


def get_num_workers():
    """
    Determine the number of worker processes based on the current time of day.
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
    Identify missing iterations for each algorithm and run them concurrently in batches.
    """
    missing_algs = {}
    found_msgs = []
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
    # Process each algorithm separately in batches.
    for alg, missing in missing_algs.items():
        start_iter = (size_results[alg][4] + 1) if size_results[alg] is not None else 1
        remaining = missing
        while remaining > 0:
            current_batch = min(BATCH_SIZE, remaining)
            tasks = {}
            with ProcessPoolExecutor(max_workers=num_workers) as executor:
                for i in range(current_batch):
                    future = executor.submit(run_iteration, algorithms()[alg], size)
                    tasks[future] = start_iter + i
                for future in as_completed(tasks):
                    iter_index = tasks[future]
                    try:
                        t = future.result()
                        with open(csv_path, "a", newline="") as csv_file:
                            writer = csv.writer(csv_file)
                            writer.writerow([alg, size, iter_index, f"{t:.8f}"])
                        if size_results[alg] is None:
                            size_results[alg] = (None, None, None, None, 0, [])
                        size_results[alg] = (
                            None,  # average to be recalculated
                            None,  # min to be recalculated
                            None,  # max to be recalculated
                            None,  # median to be recalculated
                            size_results[alg][4] + 1,
                            size_results[alg][5] + [t],
                        )
                    except Exception as e:
                        print(f"{alg} error on size {size} iteration {iter_index}: {e}")
            start_iter += current_batch
            remaining -= current_batch
            # Force garbage collection after each batch.
            gc.collect()
        # After all batches for this algorithm, recalc stats.
        times = size_results[alg][5]
        avg = compute_average(times)
        median = compute_median(times)
        size_results[alg] = (avg, min(times), max(times), median, len(times), times)
        print(f"Average for {alg} on size {size}: {format_time(avg, False)}")
        if avg > threshold and alg not in skip_list:
            skip_list[alg] = size
            print(
                f"Skipping {alg} for future sizes (average > 5min, skipped at size {size})."
            )
    # Clear temporary variables.
    del missing_algs, found_msgs
    return size_results, skip_list


def update_overall_results(
    size, size_results, expected_algs, overall_totals, per_alg_results, iterations
):
    """
    Update the aggregated overall totals and per-algorithm results for a given array size.
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
    csv_path, size_results = get_csv_results_for_size(size, expected_algs)
    current_workers = get_num_workers()
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
    sort_csv_alphabetically(csv_path)

    # Re-read to update results; no need for a local import
    _, updated_results = get_csv_results_for_size(size, expected_algs)
    update_overall_results(
        size,
        updated_results,
        expected_algs,
        overall_totals,
        per_alg_results,
        iterations,
    )
    del csv_path, updated_results
    return size_results, skip_list


def run_sorting_tests(iterations=250, threshold=300):
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
    initial_workers = get_num_workers()
    print(f"Using {initial_workers} worker{'s' if initial_workers > 1 else ''}.")
    process_size.workers = initial_workers
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
        del size_results
        # Write markdown details and rebuild README.
        _, current_results = get_csv_results_for_size(size, expected_algs)
        previous_skip = set(skip_list.keys())
        for alg, data in current_results.items():
            if data is not None and data[0] > threshold and alg not in skip_list:
                skip_list[alg] = size
        new_skipped = {
            alg: skip_list[alg] for alg in skip_list if alg not in previous_skip
        }
        with open(details_path, "a") as f:
            write_markdown(f, size, current_results, removed=list(new_skipped.keys()))
        rebuild_readme(overall_totals, details_path, skip_list)
        del current_results, previous_skip, new_skipped
        gc.collect()  # Collect garbage after processing each size.
    del sizes, expected_algs
    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

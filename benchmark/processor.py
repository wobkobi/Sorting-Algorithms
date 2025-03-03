import os
import sys
from csv_utils import get_csv_results_for_size, sort_csv_alphabetically
from markdown_utils import rebuild_readme, write_markdown, write_algorithm_markdown
from benchmark.sizes import generate_sizes, get_num_workers
from benchmark.scheduler import update_missing_iterations_concurrent
from exit_handlers import shutdown_requested
from utils import format_time


def update_overall_results(
    size, size_results, expected_algs, overall_totals, per_alg_results, iterations
):
    """
    Update cumulative benchmark results after processing a given array size.
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
    per_run_timeout=False,
):
    """
    Process benchmarking for a single array size.
    """
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
                f"Changing workers from {process_size.workers} to {current_workers} worker{'s' if current_workers > 1 else ''}."
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
        per_run_timeout,
    )
    sort_csv_alphabetically(csv_path)
    _, updated_results = get_csv_results_for_size(size, expected_algs)
    update_overall_results(
        size,
        updated_results,
        expected_algs,
        overall_totals,
        per_alg_results,
        iterations,
    )

    for alg, data in updated_results.items():
        if data is not None and data[0] > threshold and alg not in skip_list:
            skip_list[alg] = size
    return size_results, skip_list


def run_sorting_tests(iterations=500, threshold=300, per_run_timeout=False):
    """
    Execute benchmark tests over multiple array sizes and generate reports.
    """
    from algorithms_map import get_algorithms  # local import for expected_algs

    sizes = generate_sizes()
    expected_algs = list(get_algorithms().keys())
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

    try:
        for size in sizes:
            if shutdown_requested:
                print("Shutdown requested. Exiting the size loop.")
                sys.exit(0)
            print(f"\nTesting array size: {size}")
            size_results, skip_list = process_size(
                size,
                iterations,
                threshold,
                expected_algs,
                overall_totals,
                per_alg_results,
                skip_list,
                per_run_timeout=per_run_timeout,
            )
            # Additional check to skip algorithms if they exceed the threshold.
            for alg, data in size_results.items():
                if data is not None and data[0] > threshold and alg not in skip_list:
                    skip_list[alg] = size
            with open(details_path, "a") as f:
                write_markdown(f, size, size_results, skip_list)
            rebuild_readme(overall_totals, details_path, skip_list)
    except KeyboardInterrupt:
        print("KeyboardInterrupt detected. Exiting gracefully.")
        sys.exit(0)

    write_algorithm_markdown(per_alg_results)
    print(
        "\nBenchmark complete: CSV files saved, README.md updated, and per-algorithm files created in 'results/algorithms'."
    )

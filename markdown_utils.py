import os
from utils import format_time, group_rankings


def write_markdown(md_file, size, size_results):
    """
    Write the per-size ranking table to the main Markdown file (README.md).
    This table shows only the average time for each algorithm.

    Parameters:
        md_file: Open file handle for the main Markdown file.
        size (int): Current array size.
        size_results (dict): Mapping from algorithm name to (avg, min, max) tuple.
    """
    md_file.write(f"## Array Size: {size}\n")
    # Build a ranking list: (algorithm, average time)
    ranking = [(alg, data[0]) for alg, data in size_results.items() if data is not None]
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
                # Use the first algorithm's average as representative.
                rep_alg = group[0][0]
                rep_avg = next((avg for alg, avg in ranking if alg == rep_alg), None)
                algs_in_group = ", ".join(alg for alg, _ in group)
                rank_str = (
                    f"{start_rank}"
                    if start_rank == end_rank
                    else f"{start_rank}-{end_rank}"
                )
                md_file.write(
                    f"| {rank_str} | {algs_in_group} | {format_time(rep_avg)} |\n"
                )
                current_rank = end_rank + 1
            md_file.write("\n")
    else:
        md_file.write("No algorithms produced a result for this array size.\n\n")
    md_file.flush()


def write_algorithm_markdown(per_alg_results):
    """
    Write separate Markdown files for each algorithm summarizing results across sizes.

    Each file is named after the algorithm (with spaces replaced by underscores)
    and placed in the folder 'results/algorithms'. The table in each file shows the
    array size along with the average, minimum, and maximum times.

    This function will create the file only if it does not already exist.

    Parameters:
        per_alg_results (dict): Mapping from algorithm to a list of tuples (size, avg, min, max).
    """
    alg_folder = os.path.join("results", "algorithms")
    os.makedirs(alg_folder, exist_ok=True)
    for alg, results in per_alg_results.items():
        filename = f"{alg.replace(' ', '_')}.md"
        filepath = os.path.join(alg_folder, filename)
        # Create file if it doesn't exist.
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                f.write(f"# {alg} Benchmark Results\n\n")
                f.write("| Array Size | Average Time | Min Time | Max Time |\n")
                f.write("| ---------- | ------------ | -------- | -------- |\n")
                for size, avg, mn, mx in sorted(results, key=lambda x: x[0]):
                    f.write(
                        f"| {size} | {format_time(avg)} | {format_time(mn)} | {format_time(mx)} |\n"
                    )
                f.write("\n")
            print(f"Wrote results for {alg} to {filepath}")
        else:
            print(f"Markdown file for {alg} already exists; skipping.")

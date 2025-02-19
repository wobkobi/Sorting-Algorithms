import os
from utils import format_time, group_rankings


def write_markdown(md_file, size, size_results):
    """
    Write the per-size ranking table (including average, min, and max times) to the Markdown file.

    Parameters:
        md_file: Open file handle for Markdown.
        size (int): Current array size.
        size_results (dict): Mapping from algorithm to (avg, min, max) tuple.
    """
    md_file.write(f"## Array Size: {size}\n")
    ranking = [
        (alg, data[0], data[1], data[2])
        for alg, data in size_results.items()
        if data is not None
    ]
    if ranking:
        if all(t < 1e-3 for _, t, _, _ in ranking):
            md_file.write(
                "All algorithms ran in less than 1 millisecond on this array size; detailed ranking differences are negligible.\n\n"
            )
        else:
            ranking.sort(key=lambda x: x[1])
            groups = group_rankings(
                [(alg, avg) for alg, avg, mn, mx in ranking], margin=1e-3
            )
            current_rank = 1
            md_file.write(
                "| Rank | Algorithm(s) | Average Time | Min Time | Max Time |\n"
            )
            md_file.write(
                "| ---- | ------------ | ------------ | -------- | -------- |\n"
            )
            for group in groups:
                start_rank = current_rank
                end_rank = current_rank + len(group) - 1
                rep_alg = group[0][0]
                rep_avg = next(
                    (avg for alg, avg, mn, mx in ranking if alg == rep_alg), None
                )
                group_mins = [
                    mn for alg, avg, mn, mx in ranking if alg in [g[0] for g in group]
                ]
                group_maxs = [
                    mx for alg, avg, mn, mx in ranking if alg in [g[0] for g in group]
                ]
                group_min = min(group_mins) if group_mins else None
                group_max = max(group_maxs) if group_maxs else None
                algs_in_group = ", ".join(alg for alg, _ in group)
                rank_str = (
                    f"{start_rank}"
                    if start_rank == end_rank
                    else f"{start_rank}-{end_rank}"
                )
                md_file.write(
                    f"| {rank_str} | {algs_in_group} | {format_time(rep_avg)} | {format_time(group_min)} | {format_time(group_max)} |\n"
                )
                current_rank = end_rank + 1
            md_file.write("\n")
    else:
        md_file.write("No algorithms produced a result for this array size.\n\n")
    md_file.flush()


def write_algorithm_markdown(per_alg_results):
    """
    Write a separate Markdown file for each algorithm showing its results across sizes.
    If a file for an algorithm already exists in 'results/algorithms', do not overwrite it.

    Parameters:
        per_alg_results (dict): Mapping from algorithm to a list of tuples (size, avg, min, max).
    """
    alg_folder = os.path.join("results", "algorithms")
    os.makedirs(alg_folder, exist_ok=True)
    for alg, results in per_alg_results.items():
        filename = f"{alg.replace(' ', '_')}.md"
        filepath = os.path.join(alg_folder, filename)
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

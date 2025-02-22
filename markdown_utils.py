import os
from utils import format_time, group_rankings


def write_markdown(md_file, size, size_results):
    """
    Write a per-size ranking table (averages only) to the given Markdown file.

    Parameters:
        md_file: Open file handle.
        size (int): Array size.
        size_results (dict): Mapping {algorithm: (avg, min, max)}.
    """
    md_file.write(f"## Array Size: {size}\n")
    ranking = [(alg, data[0]) for alg, data in size_results.items() if data is not None]
    if ranking:
        if all(t < 1e-3 for _, t in ranking):
            md_file.write(
                "All algorithms ran in less than 1ms on this array size; differences are negligible.\n\n"
            )
        else:
            ranking.sort(key=lambda x: x[1])
            groups = group_rankings(ranking, margin=1e-3)
            current_rank = 1
            md_file.write("| Rank | Algorithm(s) | Average Time |\n")
            md_file.write("| ---- | ------------ | ------------ |\n")
            for group in groups:
                start = current_rank
                end = current_rank + len(group) - 1
                rep = group[0][1]
                algs = ", ".join(alg for alg, _ in group)
                rank_str = f"{start}" if start == end else f"{start}-{end}"
                md_file.write(f"| {rank_str} | {algs} | {format_time(rep)} |\n")
                current_rank = end + 1
            md_file.write("\n")
    else:
        md_file.write("No algorithms produced a result for this array size.\n\n")
    md_file.flush()


def write_algorithm_markdown(per_alg_results):
    """
    Write separate Markdown files for each algorithm summarizing its results.

    Each file is saved in 'results/algorithms' and contains a table with array size, average, min, and max times.
    Files are created only if they do not already exist.

    Parameters:
        per_alg_results (dict): Mapping {algorithm: [(size, avg, min, max), ...]}.
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

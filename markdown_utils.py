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


def rebuild_readme(overall_totals, details_path, skip_list):
    """
    Rebuild the main README.md using overall averages and per-size details.

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
            "The following algorithms have been removed from future sizes because their average on the current size exceeded the threshold:\n\n"
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

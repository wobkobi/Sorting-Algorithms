"""
This module provides functions for generating markdown reports based on benchmark results.

It creates per-size ranking tables, individual algorithm reports, and rebuilds the main README file.
"""

import os
from utils import format_time, group_rankings, ordinal


def write_markdown(md_file, size, size_results, removed=None):
    """
    Write a markdown table summarizing benchmark results for a specific array size.

    The table includes:
    - Rank (in ordinal format)
    - Algorithm names (grouped if their performance is nearly identical)
    - Average time
    - Median time

    If any algorithms were removed at this size (due to performance issues), a note is appended.

    Parameters:
        md_file (file object): An open file handle for writing markdown.
        size (int): The array size used for the benchmark.
        size_results (dict): Mapping {algorithm: (avg, min, max, median, count, times)}.
        removed (list, optional): List of algorithm names removed at this size.
    """
    # Write the header for the current array size.
    md_file.write(f"# Detailed Benchmark Results\n\n")
    md_file.write(f"## Array Size: {size}\n\n")
    ranking = [
        (alg, data[0], data[3])
        for alg, data in size_results.items()
        if data is not None
    ]

    if ranking:
        # If every algorithm ran extremely fast, note that differences are negligible.
        if all(t < 1e-3 for _, t, _ in ranking):
            md_file.write(
                "All algorithms ran in less than 1ms on this array size; differences are negligible.\n\n"
            )
        else:
            ranking.sort(key=lambda x: x[1])
            groups = group_rankings(ranking, margin=1e-3)
            current_rank = 1
            md_file.write("| Rank | Algorithm(s) | Average Time | Median Time |\n")
            md_file.write("| ---- | ------------ | ------------ | ----------- |\n")
            for group in groups:
                rank_str = ordinal(current_rank)
                algs = ", ".join(alg for alg, _, _ in group)
                avg_time = group[0][1]
                median_time = group[0][2]
                md_file.write(
                    f"| {rank_str} | {algs} | {format_time(avg_time, False)} | {format_time(median_time, False)} |\n"
                )
                current_rank += len(group)
            md_file.write("\n")
    else:
        md_file.write("No algorithms produced a result for this array size.\n\n")

    if removed:
        md_file.write(
            f"**Note:** The following algorithm{'s' if len(removed) != 1 else ''} were removed for this array size due to performance issues: {', '.join(sorted(removed))}.\n\n"
        )
    md_file.flush()


def write_algorithm_markdown(per_alg_results):
    """
    Generate individual markdown files summarizing benchmark results for each algorithm.

    For each algorithm, a separate markdown file is created in the "results/algorithms" directory.
    Each file contains a table that lists:
    - Array Size
    - Average Time
    - Median Time
    - Min Time
    - Max Time

    Parameters:
        per_alg_results (dict): Mapping {algorithm: [(array size, avg, min, max, median), ...]}.
    """
    alg_folder = os.path.join("results", "algorithms")
    os.makedirs(alg_folder, exist_ok=True)
    for alg, results in per_alg_results.items():
        filename = f"{alg.replace(' ', '_')}.md"
        filepath = os.path.join(alg_folder, filename)
        if not os.path.exists(filepath):
            with open(filepath, "w") as f:
                f.write(f"# {alg} Benchmark Results\n\n")
                f.write(
                    "| Array Size | Average Time | Median Time | Min Time | Max Time |\n"
                )
                f.write(
                    "| ---------- | ------------ | ----------- | -------- | -------- |\n"
                )
                for size, avg, mn, mx, median in sorted(results, key=lambda x: x[0]):
                    f.write(
                        f"| {size} | {format_time(avg, False)} | {format_time(median, False)} | {format_time(mn, False)} | {format_time(mx, False)} |\n"
                    )
                f.write("\n")
            print(f"Wrote results for {alg} to {filepath}")
        else:
            print(f"Markdown file for {alg} already exists; skipping.")


def rebuild_readme(overall_totals, details_path, skip_list):
    """
    Rebuild the main README.md file using aggregated benchmark results and detailed per-size reports.

    The README includes:
    - A title and introduction.
    - An overall top 20 ranking of algorithms (by average time across sizes), with tied algorithms grouped if necessary.
    - A table listing skipped algorithms along with the size at which each was skipped.
    - Detailed per-size benchmark information from the details file.

    Parameters:
        overall_totals (dict): Mapping {algorithm: {"sum": total_time, "count": iterations}}.
        details_path (str): Path to the markdown file containing per-size details.
        skip_list (dict): Dictionary mapping algorithm names to the size at which they were skipped.
    """
    overall = {}
    for alg, totals in overall_totals.items():
        if totals["count"] > 0:
            overall[alg] = totals["sum"] / totals["count"]

    overall_ranking = sorted(overall.items(), key=lambda x: x[1])
    groups = group_rankings(overall_ranking, margin=1e-6)

    lines = []
    lines.append("# Sorting Algorithms Benchmark Results\n\n")
    lines.append("## Overall Top 20 Algorithms (by average time across sizes)\n\n")
    lines.append("| Rank | Algorithms | Overall Average Time |\n")
    lines.append("| ---- | ---------- | -------------------- |\n")

    current_rank = 1
    printed_count = 0
    for group in groups:
        if printed_count < 20:
            rank_str = ordinal(current_rank)
            algs = ", ".join(
                f"[{alg}](results/algorithms/{alg.replace(' ', '_')}.md)"
                for alg, _ in group
            )
            avg_time = group[0][1]
            lines.append(f"| {rank_str} | {algs} | {format_time(avg_time, True)} |\n")
            printed_count += len(group)
            current_rank += len(group)
        else:
            break
    lines.append("\n")
    if printed_count > 20:
        lines.append(
            "*Note: The 20th rank falls within a tie group, so all tied algorithms are shown.*\n\n"
        )
    lines.append("## Skipped Algorithms\n\n")
    if skip_list:
        lines.append("| Algorithm | Skipped At Size |\n")
        lines.append("| --------- | --------------- |\n")
        for alg in sorted(skip_list.keys()):
            lines.append(f"| {alg} | {skip_list[alg]} |\n")
        lines.append("\n")
        print(
            "Skipped Algorithms:",
            ", ".join(
                f"{alg} (at size {skip_list[alg]})" for alg in sorted(skip_list.keys())
            ),
        )
    else:
        lines.append("No algorithms were skipped.\n\n")
        print("No algorithms were skipped.")
    with open(details_path, "r") as f:
        details_content = f.read()
    with open("README.md", "w") as md_file:
        md_file.writelines(lines)
        md_file.write(details_content)
        md_file.flush()

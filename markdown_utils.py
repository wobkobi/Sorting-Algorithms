"""
markdown_utils.py

This module provides functions for generating markdown reports based on benchmark results.
It creates per-size ranking tables, individual algorithm reports, and rebuilds the main README file.
"""

import os
from utils import format_time, group_rankings, ordinal


def write_markdown(md_file, size, size_results, removed=None):
    """
    Write a markdown table summarizing benchmark results for a specific array size.

    The table includes:
      - Rank, algorithm names, average time, and median time.
      - Algorithms with similar performance (within a specified margin) are grouped together.

    After the table, if any algorithms were removed at this size due to performance issues,
    a note is appended listing those algorithms.

    Parameters:
        md_file (file object): Open file handle for writing markdown.
        size (int): The array size used for the benchmark.
        size_results (dict): Mapping {algorithm: (avg, min, max, median, count, times)}.
        removed (list, optional): List of algorithm names removed at this size.
    """
    # Write the title followed by a blank line.
    md_file.write(f"## Array Size: {size}\n\n")
    ranking = [
        (alg, data[0], data[3])
        for alg, data in size_results.items()
        if data is not None
    ]
    if ranking:
        ranking.sort(key=lambda x: x[1])
        groups = group_rankings(ranking, margin=1e-3)
        current_rank = 1
        md_file.write("| Rank | Algorithm(s) | Average Time | Median Time |\n")
        md_file.write("| ---- | ------------ | ------------ | ----------- |\n")
        for group in groups:
            # Determine the rank for the group (using ordinal format).
            rank_str = ordinal(current_rank)
            algs = ", ".join(alg for alg, _, _ in group)
            avg_time = group[0][1]
            median_time = group[0][2]
            md_file.write(
                f"| {rank_str} | {algs} | {format_time(avg_time)} | {format_time(median_time)} |\n"
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

    Each algorithm's file is created in the "results/algorithms" directory (if it doesn't already exist)
    and contains a table listing:
      - Array Size, Average Time, Median Time, Min Time, and Max Time.

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
                        f"| {size} | {format_time(avg)} | {format_time(median)} | {format_time(mn)} | {format_time(mx)} |\n"
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
      - An overall top 20 ranking of algorithms (by average time across sizes), with tied algorithms
        grouped on a single row if their average times differ by less than one microsecond.
        For example, if three algorithms are tied for 1st, they are all labeled "1st"
        and the next rank will be "4th".
      - A section listing skipped algorithms (if any).
      - Detailed per-size benchmark information from the details file.

    Parameters:
        overall_totals (dict): Mapping {algorithm: {"sum": total_time, "count": iterations}}.
        details_path (str): Path to the markdown file containing per-size details.
        skip_list (set): Set of algorithm names that were skipped.
    """
    # Compute overall average times.
    overall = {}
    for alg, totals in overall_totals.items():
        if totals["count"] > 0:
            overall[alg] = totals["sum"] / totals["count"]

    # Sort algorithms by average time (lowest first).
    overall_ranking = sorted(overall.items(), key=lambda x: x[1])

    # Group algorithms if the difference between average times is less than 1e-6 seconds.
    groups = group_rankings(overall_ranking, margin=1e-6)

    lines = []
    lines.append("# Sorting Algorithms Benchmark Results\n\n")
    lines.append("## Overall Top 20 Algorithms (by average time across sizes)\n\n")
    lines.append("| Rank | Algorithms | Overall Average Time |\n")
    lines.append("| ---- | ---------- | -------------------- |\n")

    current_rank = 1
    count = 0  # Total number of algorithms printed.
    for group in groups:
        group_size = len(group)
        # Stop if we've printed 20 algorithms.
        if count >= 20:
            break
        # Convert the current rank to its ordinal representation.
        rank_str = ordinal(current_rank)
        # Combine algorithm names from the group.
        algs = ", ".join(alg for alg, _ in group)
        avg_time = group[0][1]  # All in the group share nearly the same average time.
        lines.append(f"| {rank_str} | {algs} | {format_time(avg_time,True)} |\n")
        count += group_size
        current_rank += group_size
    lines.append("\n")

    if skip_list:
        lines.append("## Skipped Algorithms\n\n")
        lines.append(
            "The following algorithms were removed from future sizes because their average exceeded the threshold:\n\n"
        )
        lines.append(", ".join(sorted(skip_list)) + "\n\n")
        print("Skipped Algorithms:", ", ".join(sorted(skip_list)))
    else:
        lines.append("## Skipped Algorithms\n\n")
        lines.append("No algorithms were skipped.\n\n")
        print("No algorithms were skipped.")

    with open(details_path, "r") as f:
        details_content = f.read()

    with open("README.md", "w") as md_file:
        md_file.writelines(lines)
        md_file.write(details_content)
        md_file.flush()

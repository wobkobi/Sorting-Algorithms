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
      - Rank, algorithm names, and average time.
      - Algorithms with similar performance (within a specified margin) are grouped together.

    After the table, if any algorithms were removed at this size due to performance issues,
    a note is appended listing those algorithms.

    Parameters:
        md_file (file object): Open file handle for writing markdown.
        size (int): The array size used for the benchmark.
        size_results (dict): Mapping {algorithm: (avg, min, max, median, count, times)}.
        removed (list, optional): List of algorithm names removed at this size.
    """
    # Write the header for this size with a blank line.
    md_file.write(f"## Array Size: {size}\n\n")
    ranking = [(alg, data[0]) for alg, data in size_results.items() if data is not None]
    if ranking:
        # If all times are extremely short.
        if all(t < 1e-3 for _, t in ranking):
            md_file.write(
                "All algorithms ran in less than 1ms on this array size; differences are negligible.\n\n"
            )
        else:
            ranking.sort(key=lambda x: x[1])
            groups = group_rankings(ranking, margin=1e-3)
            current_rank = 1
            md_file.write("| Rank | Algorithms | Average Time |\n")
            md_file.write("| ---- | ---------- | ------------ |\n")
            for group in groups:
                rank_str = ordinal(current_rank)
                algs = ", ".join(alg for alg, _ in group)
                avg_time = group[0][1]
                md_file.write(f"| {rank_str} | {algs} | {format_time(avg_time)} |\n")
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
    and contains a table that lists:
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
                        f"| {size} | {format_time(avg, True)} | {format_time(median, True)} | {format_time(mn, True)} | {format_time(mx, True)} |\n"
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
      - If the 20th spot is within a tie group, the entire group is shown and a note is added
        indicating that more than 20 algorithms are effectively tied.
      - A section listing skipped algorithms along with the size at which each was skipped.
      - Detailed per-size benchmark information from the details file.

    Parameters:
        overall_totals (dict): Mapping {algorithm: {"sum": total_time, "count": iterations}}.
        details_path (str): Path to the markdown file containing per-size details.
        skip_list (dict): Dictionary mapping algorithm names to the size at which they were skipped.
    """
    # Compute overall average times for each algorithm.
    overall = {}
    for alg, totals in overall_totals.items():
        if totals["count"] > 0:
            overall[alg] = totals["sum"] / totals["count"]

    # Sort algorithms by average time (lowest first).
    overall_ranking = sorted(overall.items(), key=lambda x: x[1])

    # Group algorithms that are tied (difference less than 1e-6 seconds).
    groups = group_rankings(overall_ranking, margin=1e-6)

    lines = []
    lines.append("# Sorting Algorithms Benchmark Results\n\n")
    lines.append("## Overall Top 20 Algorithms (by average time across sizes)\n\n")
    lines.append("| Rank | Algorithms | Overall Average Time |\n")
    lines.append("| ---- | ---------- | -------------------- |\n")

    current_rank = 1
    count = 0  # Total number of algorithms printed.
    for group in groups:
        # If adding the next group would push count over 20, still add the whole group.
        if count < 20:
            rank_str = ordinal(current_rank)
            algs = ", ".join(alg for alg, _ in group)
            avg_time = group[0][
                1
            ]  # All in the group share nearly the same average time.
            lines.append(f"| {rank_str} | {algs} | {format_time(avg_time, True)} |\n")
            count += len(group)
            current_rank += len(group)
        else:
            break
    lines.append("\n")

    # If the total number printed exceeds 20, add a note.
    if count > 20:
        lines.append(
            "*Note: The 20th rank falls within a tie group, so all tied algorithms are shown.*\n\n"
        )

    # Build the skipped algorithms section.
    if skip_list:
        lines.append("## Skipped Algorithms\n\n")
        lines.append(
            "The following algorithms were removed from future sizes because their average exceeded the threshold, along with the size at which they were skipped:\n\n"
        )
        skipped_list = [
            f"{alg} (at size {skip_list[alg]})" for alg in sorted(skip_list.keys())
        ]
        lines.append(", ".join(skipped_list) + "\n\n")
        print(
            "Skipped Algorithms:",
            ", ".join(
                f"{alg} (at size {skip_list[alg]})" for alg in sorted(skip_list.keys())
            ),
        )
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

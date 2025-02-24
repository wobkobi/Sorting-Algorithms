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

    This function writes a header for the given array size, followed by a table that shows:
      - The rank (in ordinal format),
      - The algorithm names (grouped if their performance is nearly identical),
      - The average time, and
      - The median time for each group.

    If any algorithms were removed at this size (due to performance issues), a note is added
    after the table listing those algorithms.

    Parameters:
        md_file (file object): An open file handle for writing markdown.
        size (int): The array size used for the benchmark.
        size_results (dict): Mapping {algorithm: (avg, min, max, median, count, times)}.
        removed (list, optional): List of algorithm names removed at this size.
    """
    # Write the header for the current array size and add a blank line.
    md_file.write(f"## Array Size: {size}\n\n")
    # Create a ranking list that includes algorithm name, average time, and median time.
    ranking = [
        (alg, data[0], data[3])
        for alg, data in size_results.items()
        if data is not None
    ]

    if ranking:
        # If every algorithm ran extremely fast (less than 1ms), state that differences are negligible.
        if all(t < 1e-3 for _, t, _ in ranking):
            md_file.write(
                "All algorithms ran in less than 1ms on this array size; differences are negligible.\n\n"
            )
        else:
            # Sort the ranking by average time in ascending order.
            ranking.sort(key=lambda x: x[1])
            # Group algorithms that are tied (difference < 1e-3 seconds).
            groups = group_rankings(ranking, margin=1e-3)
            current_rank = 1
            # Write the table header.
            md_file.write("| Rank | Algorithm(s) | Average Time | Median Time |\n")
            md_file.write("| ---- | ------------ | ------------ | ----------- |\n")
            # Iterate over each group and write a row for each.
            for group in groups:
                rank_str = ordinal(current_rank)
                # Join algorithm names in the group with a comma.
                algs = ", ".join(alg for alg, _, _ in group)
                # Use the average and median time from the first tuple in the group (they're tied).
                avg_time = group[0][1]
                median_time = group[0][2]
                md_file.write(
                    f"| {rank_str} | {algs} | {format_time(avg_time, False)} | {format_time(median_time, False)} |\n"
                )
                current_rank += len(group)
            md_file.write("\n")
    else:
        md_file.write("No algorithms produced a result for this array size.\n\n")

    # If any algorithms were removed at this size, append a note.
    if removed:
        md_file.write(
            f"**Note:** The following algorithm{'s' if len(removed) != 1 else ''} were removed for this array size due to performance issues: {', '.join(sorted(removed))}.\n\n"
        )
    md_file.flush()


def write_algorithm_markdown(per_alg_results):
    """
    Generate individual markdown files summarizing benchmark results for each algorithm.

    For each algorithm, a separate markdown file is created (if it doesn't already exist)
    in the "results/algorithms" directory. Each file contains a table that lists:
      - Array Size, Average Time, Median Time, Min Time, and Max Time for that algorithm.

    Parameters:
        per_alg_results (dict): Mapping {algorithm: [(array size, avg, min, max, median), ...]}.
    """
    alg_folder = os.path.join("results", "algorithms")
    os.makedirs(alg_folder, exist_ok=True)
    for alg, results in per_alg_results.items():
        filename = f"{alg.replace(' ', '_')}.md"
        filepath = os.path.join(alg_folder, filename)
        # Only write the file if it does not already exist.
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
      - An overall top 20 ranking of algorithms (by average time across sizes), with tied algorithms
        grouped on a single row if their average times differ by less than one microsecond.
        For example, if three algorithms are tied for 1st, they are all labeled "1st"
        and the next rank will be "4th".
      - If the 20th spot falls within a tie group, the entire group is shown and a note is added
        indicating that more than 20 algorithms are effectively tied.
      - A table listing skipped algorithms along with the size at which each was skipped.
      - Detailed per-size benchmark information from the details file.

    Parameters:
        overall_totals (dict): Mapping {algorithm: {"sum": total_time, "count": iterations}}.
        details_path (str): Path to the markdown file containing per-size details.
        skip_list (dict): Dictionary mapping algorithm names to the size at which they were skipped.
    """
    # Calculate overall average times for each algorithm.
    overall = {}
    for alg, totals in overall_totals.items():
        if totals["count"] > 0:
            overall[alg] = totals["sum"] / totals["count"]

    # Sort the overall averages in ascending order.
    overall_ranking = sorted(overall.items(), key=lambda x: x[1])

    # Group algorithms by ties (if the difference is less than 1e-6 seconds).
    groups = group_rankings(overall_ranking, margin=1e-6)

    lines = []
    lines.append("# Sorting Algorithms Benchmark Results\n\n")
    lines.append("## Overall Top 20 Algorithms (by average time across sizes)\n\n")
    lines.append("| Rank | Algorithms | Overall Average Time |\n")
    lines.append("| ---- | ---------- | -------------------- |\n")

    current_rank = 1
    printed_count = 0  # Total number of algorithms printed in the ranking.
    # Iterate through each tie group.
    for group in groups:
        # Check if printing this group will cause us to exceed 20 algorithms.
        if printed_count < 20:
            # Always print the entire tie group even if it pushes the count over 20.
            rank_str = ordinal(current_rank)
            algs = ", ".join(alg for alg, _ in group)
            avg_time = group[0][1]  # They share nearly the same average time.
            lines.append(f"| {rank_str} | {algs} | {format_time(avg_time, True)} |\n")
            printed_count += len(group)
            current_rank += len(group)
        else:
            break
    lines.append("\n")

    # Add a note if the printed count exceeds 20 (i.e. if the 20th rank falls within a tie group).
    if printed_count > 20:
        lines.append(
            "*Note: The 20th rank falls within a tie group, so all tied algorithms are shown.*\n\n"
        )

    # Build a table for skipped algorithms.
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

    # Read the per-size details from the details file.
    with open(details_path, "r") as f:
        details_content = f.read()

    # Write the final README content.
    with open("README.md", "w") as md_file:
        md_file.writelines(lines)
        md_file.write(details_content)
        md_file.flush()

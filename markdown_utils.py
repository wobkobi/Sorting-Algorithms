"""
This module provides functions for generating markdown reports based on benchmark results.

It creates per-array-size ranking tables, individual algorithm reports, and rebuilds the main README file.
"""

import os
from utils import format_time, group_rankings, ordinal


def write_markdown(md_file, size, size_results, skip_list):
    """
    Write a markdown table summarizing benchmark results for a given array size.

    This function creates a table that ranks algorithms (by average runtime)
    and displays:
      - The rank (using ordinal numbering),
      - The algorithm names (grouped if their performance is nearly identical),
      - The average time,
      - The median time.

    Algorithms that are present in the skip_list (i.e. those that were skipped)
    are excluded from the ranking table.

    Parameters:
        md_file (file object): Open file handle for writing the markdown report.
        size (int): The array size that was benchmarked.
        size_results (dict): Mapping from algorithm name to a tuple:
                             (avg, min, max, median, count, times)
                             where 'count' is the total number of iterations,
                             and 'times' is the list of iteration times.
        skip_list (dict): Mapping of algorithm names that were skipped (key) with the array size at which they were skipped.
    """
    # If this is the first write to "details.md", add the main header.
    if md_file.tell() == 0 and os.path.basename(md_file.name) == "details.md":
        md_file.write("# Detailed Benchmark Results\n\n")
    # Write header for current array size.
    md_file.write(f"## Array Size: {size}\n\n")

    # Build a ranking list excluding any skipped algorithms.
    ranking = [
        (alg, data[0], data[3])
        for alg, data in size_results.items()
        if data is not None and alg not in skip_list
    ]

    if ranking:
        # If all average times are extremely small, note that differences are negligible.
        if all(t < 1e-3 for _, t, _ in ranking):
            md_file.write(
                "All algorithms ran in less than 1ms on this array size; differences are negligible.\n\n"
            )
        else:
            ranking.sort(key=lambda x: x[1])
            # Group algorithms whose performance is nearly identical.
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

    # If there are any skipped algorithms, append a note with their names and the size they were skipped.
    if skip_list:
        md_file.write(
            f"**Note:** The following algorithm{'s' if len(skip_list) != 1 else ''} were removed for this array size due to performance issues: {', '.join(sorted(f'{alg} (at size {skip_list[alg]})' for alg in skip_list))}.\n\n"
        )
    md_file.flush()


def write_algorithm_markdown(per_alg_results):
    """
    Generate individual markdown files for each algorithm summarizing their benchmark results.

    For each algorithm, this function creates a markdown file (if one does not already exist)
    in the "results/algorithms" directory. Each file contains a table with:
      - Array Size,
      - Average Time,
      - Median Time,
      - Minimum Time,
      - Maximum Time.

    Parameters:
        per_alg_results (dict): Mapping from algorithm name to a list of tuples:
                                  [(array size, avg, min, max, median), ...].
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
    Rebuild the main README.md file using aggregated benchmark results and per-size details.

    The README includes:
      - A title and an introduction.
      - An overall top-20 ranking of algorithms (by average time across sizes), with
        algorithms tied in performance grouped together.
      - A table listing skipped algorithms and the array sizes at which they were skipped.
      - Detailed per-size benchmark information (read from the details file).

    Parameters:
        overall_totals (dict): Mapping from algorithm name to a dictionary with keys "sum" and "count".
        details_path (str): Path to the markdown file that contains detailed per-size reports.
        skip_list (dict): Mapping of algorithm names that were skipped (with corresponding array size).
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
            # Exclude skipped algorithms from the overall ranking.
            algs = ", ".join(
                f"[{alg}](results/algorithms/{alg.replace(' ', '_')}.md)"
                for alg, _ in group
                if alg not in skip_list
            )
            if algs:
                avg_time = group[0][1]
                lines.append(
                    f"| {rank_str} | {algs} | {format_time(avg_time, True)} |\n"
                )
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

    # Read detailed per-size markdown content.
    with open(details_path, "r") as f:
        details_content = f.read()
    # Adjust header levels for inclusion in README.md.
    details_content = details_content.replace(
        "# Detailed Benchmark Results", "## Detailed Benchmark Results", 1
    )
    details_content = details_content.replace("## Array Size:", "### Array Size:")

    with open("README.md", "w") as md_file:
        md_file.writelines(lines)
        md_file.write(details_content)
        md_file.flush()

"""
markdown_utils.py

This module generates markdown reports based on benchmark results.
It provides functions to:
  - Write per-array-size benchmark result tables.
  - Create individual algorithm report files.
  - Rebuild the main README.md file using aggregated benchmark data.
  
Functions:
    write_markdown(md_file, size, size_results, skip_list)
    write_algorithm_markdown(per_alg_results)
    rebuild_readme(overall_totals, details_path, skip_list)
"""

import os
from utils import format_time, group_rankings, ordinal


def write_markdown(md_file, size, size_results, skip_list):
    """
    Write a markdown section summarizing benchmark results for a specific array size.

    Creates a table that ranks algorithms by average runtime (excluding skipped ones).
    If all times are extremely small, a note is added to indicate negligible differences.

    Parameters:
        md_file (file object): Open file for writing markdown content.
        size (int): The array size benchmarked.
        size_results (dict): Mapping from algorithm to performance tuple:
                             (avg, min, max, median, count, times).
        skip_list (dict): Mapping of algorithms that were skipped (with corresponding size).
    """
    # Add main header if the file is empty and named "details.md".
    if md_file.tell() == 0 and os.path.basename(md_file.name) == "details.md":
        md_file.write("# Detailed Benchmark Results\n\n")
    md_file.write(f"## Array Size: {size}\n\n")

    # Create ranking data excluding skipped algorithms.
    ranking = [
        (alg, data[0], data[3])
        for alg, data in size_results.items()
        if data is not None and alg not in skip_list
    ]

    if ranking:
        # Note negligible differences if all average times are very small.
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

    # Append note for any skipped algorithms.
    if skip_list:
        md_file.write(
            f"**Note:** The following algorithm{'s' if len(skip_list) != 1 else ''} were removed for this array size due to performance issues: "
            + ", ".join(
                sorted(f"{alg} (at size {skip_list[alg]})" for alg in skip_list)
            )
            + "\n\n"
        )
    md_file.flush()


def write_algorithm_markdown(per_alg_results):
    """
    Generate individual markdown files for each algorithm summarizing their benchmark results.

    For each algorithm, a file is created (if it doesn't already exist) in the "results/algorithms" folder.
    Each file includes a table with:
      - Array Size, Average Time, Median Time, Min Time, and Max Time.

    Parameters:
        per_alg_results (dict): Mapping from algorithm name to a list of result tuples:
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
    Rebuild the main README.md file using overall benchmark results and detailed per-size data.

    The README includes:
      - A title and introduction.
      - An overall top-20 ranking table (with groups for tied performance).
      - A section listing skipped algorithms with the array sizes at which they were skipped.
      - Detailed per-size benchmark information read from the details file.

    Parameters:
        overall_totals (dict): Mapping from algorithm name to dict with keys "sum" and "count".
        details_path (str): Path to the markdown file containing per-size details.
        skip_list (dict): Mapping of skipped algorithms (with their respective skipped size).
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
            # Exclude algorithms that were skipped from the overall ranking.
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

    # Include detailed per-size markdown content.
    with open(details_path, "r") as f:
        details_content = f.read()
    # Adjust header levels for proper nesting.
    details_content = details_content.replace(
        "# Detailed Benchmark Results", "## Detailed Benchmark Results", 1
    )
    details_content = details_content.replace("## Array Size:", "### Array Size:")

    with open("README.md", "w") as md_file:
        md_file.writelines(lines)
        md_file.write(details_content)
        md_file.flush()

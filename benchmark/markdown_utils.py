"""
markdown_utils.py

Module for generating markdown reports from benchmark results.

Provides functions to:
  - Write per-array-size benchmark results as markdown tables.
  - Create individual markdown files for each algorithm.
  - Rebuild the main README.md file using aggregated benchmark data.
"""

import os
from .utils import format_size, format_time, group_rankings, ordinal
from .config import debug


def write_markdown(md_file, size, size_results, skip_list):
    """
    Write a markdown section summarizing benchmark results for a specific array size.

    The function generates a table that ranks algorithms by average runtime,
    and appends notes about algorithms that were skipped due to performance issues.

    Parameters:
      md_file (file object): Open file for writing markdown.
      size (int): Array size used in the benchmark.
      size_results (dict): Mapping from algorithm name to a tuple with performance data.
      skip_list (dict): Mapping of skipped algorithms and their corresponding size.
    """
    debug(f"Writing markdown for array size {format_size(size)}")
    # If this is the first write and the file is "details.md", add a main header.
    if md_file.tell() == 0 and os.path.basename(md_file.name) == "details.md":
        md_file.write("# Detailed Benchmark Results\n\n")
    md_file.write(f"## Array Size: {format_size(size)}\n\n")

    # Build ranking list.
    # Include algorithms that are either not in skip_list or that are removed at the current size.
    ranking = [
        (alg, data[0], data[3])
        for alg, data in size_results.items()
        if data is not None and (alg not in skip_list or skip_list[alg] == size)
    ]
    debug(f"Ranking data for size {format_size(size)}: {ranking}")

    if ranking:
        # If all times are extremely small, note that differences are negligible.
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

    # Determine which algorithms are removed at this specific array size.
    removed_here = [
        alg for alg, removal_size in skip_list.items() if removal_size == size
    ]
    if removed_here:
        note = (
            f"**Note:** The following algorithm{'s' if len(removed_here) != 1 else ''} "
            "were removed for this array size due to performance issues: "
            + ", ".join(
                f"{alg} (at size {format_size(skip_list[alg])})"
                for alg in sorted(removed_here)
            )
            + "\n\n"
        )
        md_file.write(note)
        debug(f"Skipped algorithms at size {format_size(size)}: {removed_here}")
    md_file.flush()


def write_algorithm_markdown(per_alg_results):
    """
    Generate individual markdown files for each algorithm with their benchmark results.

    Creates a file in the "results/algorithms" directory for each algorithm, containing
    a table of results across different array sizes.

    Parameters:
      per_alg_results (dict): Mapping from algorithm name to a list of tuples:
                              [(array size, avg, min, max, median), ...].
    """
    alg_folder = os.path.join("results", "algorithms")
    os.makedirs(alg_folder, exist_ok=True)
    debug(f"Writing individual algorithm markdown files in folder: {alg_folder}")
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
                        f"| {format_size(size)} | {format_time(avg, False)} | {format_time(median, False)} | {format_time(mn, False)} | {format_time(mx, False)} |\n"
                    )
                f.write("\n")
            print(f"Wrote results for {alg} to {filepath}")
        else:
            print(f"Markdown file for {alg} already exists; skipping.")


def rebuild_readme(overall_totals, details_path, skip_list):
    """
    Rebuild the main README.md file using aggregated benchmark data.

    The README includes:
      - Overall top-20 algorithm rankings by average time.
      - A table of skipped algorithms and their corresponding array sizes.
      - Detailed per-array-size benchmark data from the details file.

    Parameters:
      overall_totals (dict): Aggregated benchmark results per algorithm.
      details_path (str): Path to the detailed markdown file.
      skip_list (dict): Mapping of skipped algorithms with the array size at which they were skipped.
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
            # Link to individual algorithm markdown files, excluding skipped algorithms.
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

    # Append detailed per-size markdown content.
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
    debug("Rebuilt README.md with overall benchmark results.")

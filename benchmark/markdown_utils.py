"""
markdown_utils.py

Module for generating markdown reports from benchmark results.

Provides functions to:
  - Write per-array-size benchmark results as markdown tables (with an optional Variance (%) column).
  - Create individual markdown files for each algorithm.
  - Rebuild the main README.md file using aggregated benchmark data and a Table of Contents.
"""

import os
import re
from .utils import format_size, format_time, group_rankings, ordinal, compute_variance
from .config import debug


def write_markdown(md_file, size, size_results, skip_list):
    """
    Write a markdown section summarizing benchmark results for a specific array size.

    Generates a table ranking algorithms by average runtime and includes an extra column
    for variance percentage. Variance is computed as ((max - min) / avg) * 100 for a group
    with a single algorithm. For groups (ties) with multiple algorithms, the Variance column
    is left blank.

    If any algorithms are removed at this array size due to performance issues, a note is appended.

    Parameters:
      md_file (file object): Open file for writing markdown.
      size (int): Array size used in the benchmark.
      size_results (dict): Mapping from algorithm name to a tuple with performance data
                           in the form (avg, min, max, median, count, times_list).
      skip_list (dict): Mapping of algorithms to the array size at which they were removed.
                        An algorithm removed at this size is included in the ranking.
    """
    debug(f"Writing markdown for array size {format_size(size)}")
    if md_file.tell() == 0 and os.path.basename(md_file.name) == "details.md":
        # Write main header and column explanation.
        md_file.write("# Detailed Benchmark Results\n\n")
        md_file.write(
            "Below is a table of benchmark results for each array size. "
            "The columns are defined as follows:\n\n"
        )
        md_file.write("- **Rank:** The ranking order based on average runtime.\n")
        md_file.write(
            "- **Algorithm(s):** The name(s) of the algorithm(s). Ties indicate algorithms with similar performance.\n"
        )
        md_file.write(
            "- **Average Time:** The average runtime for the algorithm over all iterations.\n"
        )
        md_file.write("- **Median Time:** The median runtime for the algorithm.\n")
        md_file.write(
            "- **Variance (%):** The percentage difference between the maximum and minimum runtimes relative to the average. "
            + "A **lower variance** (typically below 10%) indicates that the algorithm's performance is very consistent across iterations, "
            + "whereas a **higher variance** (often above 50%) suggests that its performance is more variable. "
            + "This column is only shown for algorithms that do not share a ranking (i.e. no tie).\n\n"
        )

    md_file.write(f"## Array Size: {format_size(size)}\n\n")

    # Build ranking list: include algorithm if not skipped or if skipped exactly at this size.
    ranking = [
        (alg, data[0], data[1], data[2], data[3])
        for alg, data in size_results.items()
        if data is not None and (alg not in skip_list or skip_list[alg] == size)
    ]
    debug(f"Ranking data for size {format_size(size)}: {ranking}")

    if ranking:
        if all(t < 1e-3 for _, t, _, _, _ in ranking):
            md_file.write(
                "All algorithms ran in less than 1ms on this array size; differences are negligible.\n\n"
            )
        else:
            ranking.sort(key=lambda x: x[1])  # sort by average time
            groups = group_rankings(ranking, margin=1e-3)
            current_rank = 1
            # Write header with extra "Variance (%)" column.
            md_file.write(
                "| Rank | Algorithm(s) | Average Time | Median Time | Variance (%) |\n"
            )
            md_file.write(
                "| ---- | ------------ | ------------ | ----------- | ------------ |\n"
            )
            for group in groups:
                rank_str = ordinal(current_rank)
                algs = ", ".join(alg for alg, _, _, _, _ in group)
                avg_time = group[0][1]
                min_time = group[0][2]
                max_time = group[0][3]
                median_time = group[0][4]
                # Only compute variance if the group has a single algorithm.
                if len(group) == 1:
                    variance = compute_variance(avg_time, min_time, max_time)
                    variance_str = f"{variance:.0f}%" if variance is not None else "N/A"
                else:
                    variance_str = ""
                md_file.write(
                    f"| {rank_str} | {algs} | {format_time(avg_time, False)} | {format_time(median_time, False)} | {variance_str} |\n"
                )
                current_rank += len(group)
            md_file.write("\n")
    else:
        md_file.write("No algorithms produced a result for this array size.\n\n")

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
    a table of results across different array sizes. An extra column "Variance (%)" is added,
    but only for rows without ties.

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
                # Explanation for each column.
                f.write(
                    "The table below shows benchmark results for various array sizes.\n\n"
                )
                f.write("- **Array Size:** The number of elements sorted.\n")
                f.write(
                    "- **Average Time:** The average runtime for the algorithm at that array size.\n"
                )
                f.write("- **Median Time:** The median runtime for the algorithm.\n")
                f.write("- **Min Time:** The fastest recorded runtime.\n")
                f.write("- **Max Time:** The slowest recorded runtime.\n")
                f.write(
                    "- **Variance (%):** The percentage difference between the max and min runtimes relative to the average. "
                    "This column is left blank if there are ties for that array size.\n\n"
                )
                f.write(
                    "| Array Size | Average Time | Median Time | Min Time | Max Time | Variance (%) |\n"
                )
                f.write(
                    "| ---------- | ------------ | ----------- | -------- | -------- | ------------ |\n"
                )
                for size, avg, mn, mx, median in sorted(results, key=lambda x: x[0]):
                    if avg and avg != 0:
                        variance = compute_variance(avg, mn, mx)
                        variance_str = (
                            f"{variance:.0f}%" if variance is not None else "N/A"
                        )
                    else:
                        variance_str = "N/A"
                    f.write(
                        f"| {format_size(size)} | {format_time(avg, False)} | {format_time(median, False)} | "
                        f"{format_time(mn, False)} | {format_time(mx, False)} | {variance_str} |\n"
                    )
                f.write("\n")
            print(f"Wrote results for {alg} to {filepath}")
        else:
            print(f"Markdown file for {alg} already exists; skipping.")


def rebuild_readme(overall_totals, details_path, skip_list):
    """
    Rebuild the main README.md file using aggregated benchmark results and detailed per-size data.

    The README includes:
      - Overall Top 20 Algorithms by average time.
      - A Table of Contents (ToC) listing each array size section, placed below the top 20 table.
      - A section for Skipped Algorithms.
      - Detailed per-array-size benchmark data (read from the details file).
      - An explanation of each column is provided under the "Detailed Benchmark Results" header.

    Parameters:
      overall_totals (dict): Aggregated benchmark results per algorithm.
      details_path (str): Path to the detailed markdown file.
      skip_list (dict): Mapping of algorithms to the array size at which they were skipped.
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
            # Exclude skipped algorithms.
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

    # Build the Table of Contents (ToC) based on the details file.
    with open(details_path, "r") as f:
        details_content = f.read()
    # Adjust headers for ToC generation.
    adjusted_details = details_content.replace(
        "# Detailed Benchmark Results", "## Detailed Benchmark Results", 1
    )
    adjusted_details = adjusted_details.replace("## Array Size:", "### Array Size:")
    toc = ["## Table of Contents\n\n"]
    sizes = re.findall(r"^###\s*Array Size:\s*(.+)$", adjusted_details, re.MULTILINE)
    for s in sizes:
        anchor = "array-size-" + s.replace(",", "").strip().lower().replace(" ", "-")
        toc.append(f"- [Array Size: {s}](#{anchor})\n")
    toc.append("\n")
    lines.extend(toc)

    # Append Skipped Algorithms section.
    lines.append("## Skipped Algorithms\n\n")
    if skip_list:
        lines.append("| Algorithm | Skipped At Size |\n")
        lines.append("| --------- | --------------- |\n")
        for alg, size in sorted(skip_list.items(), key=lambda item: item[1]):
            lines.append(f"| {alg} | {size} |\n")
        lines.append("\n")
        print(
            "Skipped Algorithms:",
            ", ".join(
                f"{alg} (at size {size})"
                for alg, size in sorted(skip_list.items(), key=lambda item: item[1])
            ),
        )
    else:
        lines.append("No algorithms were skipped.\n\n")
        print("No algorithms were skipped.")

    # Append detailed per-size markdown content.
    with open(details_path, "r") as f:
        details_content_original = f.read()
    details_content_original = details_content_original.replace(
        "# Detailed Benchmark Results", "## Detailed Benchmark Results", 1
    )
    details_content_original = details_content_original.replace(
        "## Array Size:", "### Array Size:"
    )
    lines.append(details_content_original)

    with open("README.md", "w") as md_file:
        md_file.writelines(lines)
        md_file.flush()
    debug(
        "Rebuilt README.md with overall top 20, ToC, skipped algorithms, and detailed sections."
    )

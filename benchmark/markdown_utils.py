"""
markdown_utils.py

Generates markdown reports based on benchmark results.
Includes functions to write detailed sections for each array size,
generate per–algorithm reports, update the table of contents, and rebuild the README.
"""

import os
import re
from .utils import format_size, format_time, group_rankings, ordinal, compute_variance
from .config import debug

REPORT_DESCRIPTION = (
    "This benchmark report compares various sorting algorithms based on their performance across different array sizes. "
    "Each algorithm's performance is evaluated by its average and median runtimes, as well as the variance in its runtime measurements. "
    "A low variance (typically below 10%) indicates consistent performance, whereas a high variance (often above 50%) indicates that "
    "the algorithm's performance is less predictable. Algorithms that do not meet performance criteria at certain sizes are noted accordingly.\n\n"
)


def write_markdown(md_file, size, size_results, skip_list):
    """
    Write a markdown section summarizing benchmark results for a specific array size.

    Parameters:
      md_file (file object): Open file for writing markdown.
      size (int): Array size.
      size_results (dict): Performance data for each algorithm.
      skip_list (dict): Algorithms marked for skipping.
    """
    debug(f"Writing markdown for array size {format_size(size)}.")
    if md_file.tell() == 0 and os.path.basename(md_file.name) == "details.md":
        md_file.write("# Detailed Benchmark Results\n\n")
        md_file.write(REPORT_DESCRIPTION)
        md_file.write(
            "Below is a table of benchmark results for each array size. The columns are defined as follows:\n\n"
        )
        md_file.write("- **Rank:** Ranking order based on average runtime.\n")
        md_file.write(
            "- **Algorithm(s):** Name(s) of the algorithm(s); ties indicate similar performance.\n"
        )
        md_file.write("- **Average Time:** Average runtime over iterations.\n")
        md_file.write("- **Median Time:** Median runtime for the algorithm.\n")
        md_file.write(
            "- **Variance (%):** Percentage difference between maximum and minimum runtimes relative to the average. (Left blank for ties.)\n\n"
        )
    md_file.write(f"## Array Size: {format_size(size)}\n\n")
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
            ranking.sort(key=lambda x: x[1])
            groups = group_rankings(ranking, margin=1e-3)
            current_rank = 1
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
    if os.path.basename(md_file.name) == "details.md":
        update_details_with_toc(md_file.name)


def write_algorithm_markdown(per_alg_results):
    """
    Generate individual markdown files for each algorithm's benchmark results.

    Parameters:
      per_alg_results (dict): Mapping of algorithm names to a list of results tuples.
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
                f.write(REPORT_DESCRIPTION)
                f.write(
                    "The table below shows benchmark results for various array sizes.\n\n"
                )
                f.write("- **Array Size:** The number of elements sorted.\n")
                f.write(
                    "- **Average Time:** Average runtime for the algorithm at that array size.\n"
                )
                f.write("- **Median Time:** Median runtime for the algorithm.\n")
                f.write("- **Min Time:** Fastest recorded runtime.\n")
                f.write("- **Max Time:** Slowest recorded runtime.\n")
                f.write(
                    "- **Variance (%):** Percentage difference between max and min relative to average (blank if tied).\n\n"
                )
                f.write(
                    "| Array Size | Average Time | Median Time | Min Time | Max Time | Variance (%) |\n"
                )
                f.write(
                    "| ---------- | ------------ | ----------- | -------- | -------- | ------------ |\n"
                )
                for size, avg, mn, mx, median in sorted(results, key=lambda x: x[0]):
                    variance = compute_variance(avg, mn, mx)
                    variance_str = (
                        f"{variance:.0f}%"
                        if (variance is not None and avg != 0)
                        else "N/A"
                    )
                    f.write(
                        f"| {format_size(size)} | {format_time(avg, False)} | {format_time(median, False)} | "
                        f"{format_time(mn, False)} | {format_time(mx, False)} | {variance_str} |\n"
                    )
                f.write("\n")
            print(f"Wrote results for {alg} to {filepath}")
            debug(f"Wrote markdown file for {alg} at {filepath}.")
        else:
            print(f"Markdown file for {alg} already exists; skipping.")
            debug(f"Markdown file for {alg} already exists at {filepath}; skipping.")


def update_details_with_toc(details_path):
    """
    Update the Table of Contents (TOC) in details.md and ensure the report description is at the top.

    Parameters:
      details_path (str): Path to the details.md file.
    """
    with open(details_path, "r") as f:
        content = f.read()
    content = re.sub(
        r"(?s)## Table of Contents.*?(?=^## Array Size:|\Z)",
        "",
        content,
        flags=re.MULTILINE,
    )
    header_pattern = r"^# Detailed Benchmark Results\s*$"
    header_match = re.search(header_pattern, content, re.MULTILINE)
    if not header_match:
        debug("Main header not found in details.md; skipping TOC update.")
        return
    header_end = header_match.end()
    after_header = content[header_end:].lstrip()
    if not after_header.startswith(REPORT_DESCRIPTION.strip()):
        toc_marker_match = re.search(
            r"^## Table of Contents", after_header, re.MULTILINE
        )
        rest = (
            after_header[toc_marker_match.start() :]
            if toc_marker_match
            else after_header
        )
        content = (
            content[:header_end].rstrip() + "\n\n" + REPORT_DESCRIPTION + "\n" + rest
        )
    sizes = re.findall(r"^## Array Size:\s*(.+)$", content, re.MULTILINE)
    toc_lines = ["## Table of Contents", ""]
    for s in sizes:
        anchor = "array-size-" + s.replace(",", "").strip().lower().replace(" ", "-")
        toc_lines.append(f"- [Array Size: {s}](#{anchor})")
    toc_lines.append("")
    toc = "\n".join(toc_lines)
    desc_index = content.find(REPORT_DESCRIPTION.strip())
    if desc_index != -1:
        desc_end = desc_index + len(REPORT_DESCRIPTION.strip())
        before = content[:desc_end].rstrip()
        after = content[desc_end:].lstrip()
        new_content = before + "\n\n" + toc + "\n" + after
    else:
        new_content = (
            content[:header_end].rstrip()
            + "\n\n"
            + toc
            + "\n"
            + content[header_end:].lstrip()
        )
    with open(details_path, "w") as f:
        f.write(new_content)
    debug("Updated details.md with Table of Contents.")


def rebuild_readme(overall_totals, details_path, skip_list):
    """
    Rebuild the main README.md file using aggregated benchmark results and detailed markdown content.

    Parameters:
      overall_totals (dict): Aggregated results per algorithm.
      details_path (str): Path to the detailed markdown file.
      skip_list (dict): Mapping of skipped algorithms.
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
    with open(details_path, "r") as f:
        details_content = f.read()
    details_content = details_content.replace(
        "# Detailed Benchmark Results", "## Detailed Benchmark Results", 1
    )
    details_content = details_content.replace(
        "## Table of Contents", "### Table of Contents", 1
    )
    details_content = details_content.replace("## Array Size:", "### Array Size:")
    lines.append(details_content)
    with open("README.md", "w") as md_file:
        md_file.writelines(lines)
        md_file.flush()
    debug(
        "Rebuilt README.md with overall top 20, TOC, skipped algorithms, and detailed sections."
    )

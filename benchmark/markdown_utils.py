"""
markdown_utils.py

Generates markdown reports based on benchmark results.

Handles:
  - Writing detailed markdown sections for each array size.
  - Generating individual algorithm markdown report files.
  - Updating the Table of Contents (TOC) in the details markdown file.
  - Rebuilding the main README.md file with overall results, skipped algorithms, and detailed sections.

Functions:
  - write_markdown(md_file, size, size_results, skip_list):
        Writes a markdown section summarizing benchmark results for a specific array size.
  - write_algorithm_markdown(per_alg_results):
        Creates individual markdown files for each algorithm with their benchmark results.
  - update_details_with_toc(details_path):
        Updates the TOC in details.md based on current array size sections and ensures the report description is above it.
  - rebuild_readme(overall_totals, details_path, skip_list):
        Rebuilds the main README.md file using aggregated results and detailed markdown data.
"""

import os
import re
from .utils import format_size, format_time, group_rankings, ordinal, compute_variance
from .config import debug

# REPORT_DESCRIPTION explains the variance metric.
# A low variance (typically below 10%) indicates consistent performance,
# while a high variance (often above 50%) indicates unpredictable performance.
REPORT_DESCRIPTION = (
    "This benchmark report compares various sorting algorithms based on their performance across different array sizes. "
    "Each algorithm's performance is evaluated by its average and median runtimes, as well as the variance in its runtime measurements. "
    "A low variance (typically below 10%) indicates consistent performance, whereas a high variance (often above 50%) indicates that "
    "the algorithm's performance is less predictable. Algorithms that do not meet performance criteria at certain sizes are noted accordingly.\n\n"
)


def write_markdown(md_file, size, size_results, skip_list):
    """
    Write a markdown section summarizing benchmark results for a specific array size.

    This function generates a table ranking algorithms by their average runtime.
    It also includes an extra column for variance percentage for individual results.
    If an algorithm is removed at a given array size due to performance issues,
    a note is appended.

    Parameters:
      md_file (file object): Open file for writing markdown content.
      size (int): The array size used in the benchmark.
      size_results (dict): Mapping from algorithm name to a tuple containing
                           performance data in the form (avg, min, max, median, count, times_list).
      skip_list (dict): Mapping of algorithms to the array size at which they were removed.
                        An algorithm removed at this size is still included in the ranking.
    """
    debug(f"Writing markdown for array size {format_size(size)}")
    # If this is the first write to details.md, output the header, report description, and column explanations.
    if md_file.tell() == 0 and os.path.basename(md_file.name) == "details.md":
        md_file.write("# Detailed Benchmark Results\n\n")
        md_file.write(REPORT_DESCRIPTION)
        md_file.write(
            "Below is a table of benchmark results for each array size. "
            "The columns are defined as follows:\n\n"
        )
        md_file.write("- **Rank:** Ranking order based on average runtime.\n")
        md_file.write(
            "- **Algorithm(s):** Name(s) of the algorithm(s). Ties indicate similar performance.\n"
        )
        md_file.write("- **Average Time:** Average runtime over all iterations.\n")
        md_file.write("- **Median Time:** Median runtime for the algorithm.\n")
        md_file.write(
            "- **Variance (%):** Percentage difference between maximum and minimum runtimes relative to the average. "
            "For a single algorithm (no tie), a lower variance (typically below 10%) indicates consistent performance, "
            "while a higher variance (often above 50%) indicates variability. "
            "This column is left blank for ties.\n\n"
        )
    # Write the array size header as a level-2 header.
    md_file.write(f"## Array Size: {format_size(size)}\n\n")

    # Build the ranking list.
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

    # Append a note if any algorithms were skipped at this size.
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

    # Immediately update the TOC (and ensure the description appears above it) after finishing this array size section.
    if os.path.basename(md_file.name) == "details.md":
        update_details_with_toc(md_file.name)


def write_algorithm_markdown(per_alg_results):
    """
    Generate individual markdown files for each algorithm's benchmark results.

    For each algorithm, creates a file in the "results/algorithms" directory with a table of results
    across different array sizes. An extra column for "Variance (%)" is added for single algorithm rows.

    Parameters:
      per_alg_results (dict): Mapping from algorithm name to a list of tuples in the form:
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
                f.write(REPORT_DESCRIPTION)
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
                    "For a single measurement, lower variance (typically below 10%) means consistent performance, while higher "
                    "variance (often above 50%) indicates variability. This column is left blank if there are ties.\n\n"
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
        else:
            print(f"Markdown file for {alg} already exists; skipping.")


def update_details_with_toc(details_path):
    """
    Update the Table of Contents (TOC) in details.md and ensure the report description appears above it.

    This function performs the following steps:
      1. Removes any existing TOC (from the "## Table of Contents" header up to the first "## Array Size:" header).
      2. Splits the content immediately after the "# Detailed Benchmark Results" header.
      3. Forces REPORT_DESCRIPTION to appear immediately after that header.
      4. Rebuilds the TOC from all "## Array Size:" headers found in the remainder of the content.
      5. Inserts the new TOC immediately after REPORT_DESCRIPTION, ensuring one blank line above and below the TOC.

    In details.md, the TOC header is set at level 2.

    Parameters:
      details_path (str): The file path to details.md.
    """
    with open(details_path, "r") as f:
        content = f.read()

    # Remove any existing TOC section.
    content = re.sub(
        r"(?s)## Table of Contents.*?(?=^## Array Size:|\Z)",
        "",
        content,
        flags=re.MULTILINE,
    )

    # Find the main header.
    header_pattern = r"^# Detailed Benchmark Results\s*$"
    header_match = re.search(header_pattern, content, re.MULTILINE)
    if not header_match:
        debug("Main header not found in details.md; skipping TOC update.")
        return

    # Split content after the header.
    header_end = header_match.end()
    after_header = content[header_end:].lstrip()

    # Ensure REPORT_DESCRIPTION appears immediately after the header.
    if not after_header.startswith(REPORT_DESCRIPTION.strip()):
        # Remove any existing description up to the TOC marker.
        toc_marker_match = re.search(
            r"^## Table of Contents", after_header, re.MULTILINE
        )
        if toc_marker_match:
            rest = after_header[toc_marker_match.start() :]
        else:
            rest = after_header
        content = (
            content[:header_end].rstrip() + "\n\n" + REPORT_DESCRIPTION + "\n" + rest
        )

    # Build the new TOC by scanning for all "## Array Size:" headers.
    sizes = re.findall(r"^## Array Size:\s*(.+)$", content, re.MULTILINE)
    toc_lines = ["## Table of Contents", ""]
    for s in sizes:
        anchor = "array-size-" + s.replace(",", "").strip().lower().replace(" ", "-")
        toc_lines.append(f"- [Array Size: {s}](#{anchor})")
    toc_lines.append("")  # Ensure a single trailing blank line
    toc = "\n".join(toc_lines)

    # Insert the new TOC immediately after REPORT_DESCRIPTION.
    desc_index = content.find(REPORT_DESCRIPTION.strip())
    if desc_index != -1:
        desc_end = desc_index + len(REPORT_DESCRIPTION.strip())
        before = content[:desc_end].rstrip()
        after = content[desc_end:].lstrip()
        new_content = before + "\n\n" + toc + "\n" + after
    else:
        # Fallback: insert after header.
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
    Rebuild the main README.md file using aggregated benchmark results and detailed per-size data.

    The final README.md structure is as follows:
      - H1: Project title ("# Sorting Algorithms Benchmark Results")
      - H2: Overall Top 20 Algorithms table
      - H2: Skipped Algorithms section
      - H2: Detailed Benchmark Results section (sourced from details.md with headings lowered by one level):
            * "# Detailed Benchmark Results" becomes "## Detailed Benchmark Results"
            * "## Table of Contents" becomes "### Table of Contents"
            * "## Array Size:" becomes "### Array Size:"
      - The report description (REPORT_DESCRIPTION) appears only once as part of the detailed section.

    Parameters:
      overall_totals (dict): Aggregated benchmark results per algorithm.
      details_path (str): The file path to details.md.
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

    # Read the detailed markdown content from details.md and lower its headings by one level for README.
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

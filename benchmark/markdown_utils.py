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
            "For a single algorithm (no tie), a lower variance (typically below 10%) indicates consistent performance, "
            "while a higher variance (often above 50%) indicates significant variability. "
            "This column is left blank for ties.\n\n"
        )
    # Write the array size header as a level-3 header.
    md_file.write(f"### Array Size: {format_size(size)}\n\n")

    # Build ranking list: include an algorithm if it's not in skip_list or if its removal size matches the current size.
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

    # Update the TOC immediately after finishing this array size.
    if os.path.basename(md_file.name) == "details.md":
        update_details_with_toc(md_file.name)


def write_algorithm_markdown(per_alg_results):
    """
    Generate individual markdown files for each algorithm with their benchmark results.

    Creates a file in the "results/algorithms" directory for each algorithm, containing
    a table of results across different array sizes. An extra column "Variance (%)" is added,
    but only for rows without ties.
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
    Update the Table of Contents (TOC) in details.md.

    Removes any existing TOC (from the "## Table of Contents" header up to the first "### Array Size:" header)
    and inserts a fresh TOC immediately after the "# Detailed Benchmark Results" header.
    In details.md the TOC header is level 2.
    """
    with open(details_path, "r") as f:
        content = f.read()

    # Remove any existing TOC section (up to the first "### Array Size:" header).
    content = re.sub(
        r"(?s)## Table of Contents.*?(?=^### Array Size:|\Z)",
        "",
        content,
        flags=re.MULTILINE,
    )

    # Ensure the main header exists.
    header_pattern = r"^# Detailed Benchmark Results\s*$"
    header_match = re.search(header_pattern, content, re.MULTILINE)
    if not header_match:
        debug("Main header not found in details.md; skipping TOC update.")
        return

    # Build the TOC by scanning for all "### Array Size:" headers.
    sizes = re.findall(r"^### Array Size:\s*(.+)$", content, re.MULTILINE)
    toc_lines = ["## Table of Contents\n"]
    for s in sizes:
        anchor = "array-size-" + s.replace(",", "").strip().lower().replace(" ", "-")
        toc_lines.append(f"- [Array Size: {s}](#{anchor})")
    toc_lines.append("")  # Trailing blank line
    toc = "\n".join(toc_lines)

    # Insert the TOC immediately after the main header.
    header_end = header_match.end()
    new_content = (
        content[:header_end].rstrip()
        + "\n\n"
        + toc
        + "\n"  # Changed from "\n\n" to "\n" to ensure only one blank line after the TOC.
        + content[header_end:].lstrip()
    )

    with open(details_path, "w") as f:
        f.write(new_content)
    debug("Updated details.md with Table of Contents.")


def rebuild_readme(overall_totals, details_path, skip_list):
    """
    Rebuild the main README.md file using aggregated benchmark results and the detailed per-size data.

    The final README structure is:
      - H1: Project title ("# Sorting Algorithms Benchmark Results")
      - H2: Overall Top 20 Algorithms table
      - H2: Skipped Algorithms section
      - H2: Detailed Benchmark Results section (from details.md, lowered by one level):
            * "# Detailed Benchmark Results" becomes "## Detailed Benchmark Results"
            * "## Table of Contents" becomes "### Table of Contents"
            * "### Array Size:" becomes "#### Array Size:"
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

    # Read detailed per-size markdown content from details.md and lower headings by one for README.
    with open(details_path, "r") as f:
        details_content = f.read()
    details_content = details_content.replace(
        "# Detailed Benchmark Results", "## Detailed Benchmark Results", 1
    )
    details_content = details_content.replace(
        "## Table of Contents", "### Table of Contents", 1
    )
    details_content = details_content.replace("### Array Size:", "#### Array Size:")
    lines.append(details_content)

    with open("README.md", "w") as md_file:
        md_file.writelines(lines)
        md_file.flush()
    debug(
        "Rebuilt README.md with overall top 20, TOC, skipped algorithms, and detailed sections."
    )

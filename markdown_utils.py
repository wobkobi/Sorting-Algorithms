import os
from utils import format_time, group_rankings


def write_markdown(md_file, size, size_results):
    """
    Write a markdown table summarizing benchmark results for a specific array size.

    The table includes the rank, algorithm names, average time, and median time.
    Algorithms with similar performance (differences below a given margin) are grouped
    together and assigned a rank range.

    Parameters:
        md_file (file object): An open file handle to write the markdown content.
        size (int): The array size used for the benchmark.
        size_results (dict): A mapping of algorithm names to a tuple of results in the format
                             (average time, minimum time, maximum time, median time). Algorithms
                             with no results have a value of None.
    """
    md_file.write(f"## Array Size: {size}\n")
    ranking = [
        (alg, data[0], data[3])
        for alg, data in size_results.items()
        if data is not None
    ]  # Create list of tuples: (algorithm, average time, median time)

    if ranking:
        ranking.sort(key=lambda x: x[1])  # Sort by average time
        groups = group_rankings(ranking, margin=1e-3)
        current_rank = 1
        md_file.write("| Rank | Algorithm(s) | Average Time | Median Time |\n")
        md_file.write("| ---- | ------------ | ------------ | ----------- |\n")

        for group in groups:
            start = current_rank
            end = current_rank + len(group) - 1
            avg_time = group[0][1]
            median_time = group[0][2]
            algs = ", ".join(alg for alg, _, _ in group)
            rank_str = f"{start}" if start == end else f"{start}-{end}"
            md_file.write(
                f"| {rank_str} | {algs} | {format_time(avg_time)} | {format_time(median_time)} |\n"
            )
            current_rank = end + 1
        md_file.write("\n")
    else:
        md_file.write("No algorithms produced a result for this array size.\n\n")
    md_file.flush()


def write_algorithm_markdown(per_alg_results):
    """
    Generate individual markdown files summarizing benchmark results for each algorithm.

    For every algorithm, a markdown file is created (if it doesn't already exist) in the
    'results/algorithms' directory. Each file contains a table listing array size, average time,
    median time, minimum time, and maximum time for each benchmark run.

    Parameters:
        per_alg_results (dict): A mapping of algorithm names to a list of tuples containing
                                benchmark results in the format:
                                (array size, average time, minimum time, maximum time, median time).
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
    Rebuild the main README.md file using aggregated benchmark results and details.

    This function constructs an updated README that includes:
      - A title and introduction.
      - An overall top-10 ranking of algorithms based on their average benchmark time.
      - A section listing algorithms that were skipped (due to exceeding a performance threshold).
      - Detailed per-size benchmark information read from the provided details file.

    Parameters:
        overall_totals (dict): A mapping of algorithm names to dictionaries with keys "sum" and "count",
                               representing the total accumulated time and number of iterations, respectively.
        details_path (str): The file path to the markdown file containing detailed per-size results.
        skip_list (set): A set of algorithm names that were skipped for future sizes due to performance issues.
    """
    overall = {}
    for alg, totals in overall_totals.items():
        if totals["count"] > 0:
            overall[alg] = totals["sum"] / totals["count"]
    overall_ranking = sorted(overall.items(), key=lambda x: x[1])

    lines = []
    lines.append("# Sorting Algorithms Benchmark Results\n\n")
    lines.append("## Overall Top 10 Algorithms (by average time across sizes)\n")
    lines.append("| Rank | Algorithm | Overall Average Time |\n")
    lines.append("| ---- | --------- | -------------------- |\n")
    for rank, (alg, avg_time) in enumerate(overall_ranking[:10], start=1):
        link = f"[{alg}](results/algorithms/{alg.replace(' ', '_')}.md)"
        lines.append(f"| {rank} | {link} | {format_time(avg_time)} |\n")
    lines.append("\n")

    if skip_list:
        lines.append("## Skipped Algorithms\n")
        lines.append(
            "The following algorithms have been removed from future sizes because their average on the current size exceeded the threshold:\n\n"
        )
        lines.append(", ".join(sorted(skip_list)) + "\n\n")
        print("Skipped Algorithms:", ", ".join(sorted(skip_list)))
    else:
        lines.append("## Skipped Algorithms\n")
        lines.append("No algorithms were skipped.\n\n")
        print("No algorithms were skipped.")

    with open(details_path, "r") as f:
        details_content = f.read()

    with open("README.md", "w") as md_file:
        md_file.writelines(lines)
        md_file.write(details_content)
        md_file.flush()

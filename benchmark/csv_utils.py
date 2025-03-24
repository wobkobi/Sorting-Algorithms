"""
csv_utils.py

Utility functions for handling CSV files in the benchmark system.
Includes functions to read CSV results, ensure proper formatting,
sort CSV rows, and retrieve or create CSV files for given array sizes.
"""

import csv
import os
from collections import OrderedDict
from .utils import compute_average, compute_median
from .config import debug


def read_csv_results(csv_path, expected_algs, max_iterations=None):
    """
    Parse benchmark results from a CSV file and compute performance statistics.

    Parameters:
      csv_path (str): Path to the CSV file.
      expected_algs (list): List of expected algorithm names.
      max_iterations (int, optional): Maximum iterations to consider.

    Returns:
      OrderedDict: Mapping from algorithm to performance tuple.
    """
    debug(f"Reading CSV results from {csv_path}.")
    algorithm_times = OrderedDict((alg, []) for alg in expected_algs)
    try:
        with open(csv_path, "r", newline="") as csvfile:
            reader = csv.reader(csvfile)
            next(reader, None)  # Skip header.
            for row in reader:
                if not row or len(row) < 4:
                    continue
                alg = row[0]
                try:
                    iter_num = int(row[2])
                except Exception:
                    continue
                try:
                    t = float(row[3])
                except Exception:
                    continue
                if alg in algorithm_times:
                    if max_iterations is not None and iter_num > max_iterations:
                        continue
                    algorithm_times[alg].append((iter_num, t))
    except Exception as e:
        debug(f"Error reading CSV {csv_path}: {e}")

    results = OrderedDict()
    for alg in expected_algs:
        entries = algorithm_times[alg]
        entries.sort(key=lambda x: x[0])
        if max_iterations is not None:
            entries = entries[:max_iterations]
        times = [t for (_, t) in entries]
        results[alg] = (
            (
                compute_average(times),
                min(times) if times else None,
                max(times) if times else None,
                compute_median(times),
                len(times),
                times,
            )
            if times
            else None
        )
    debug(f"Completed reading CSV results from {csv_path}.")
    return results


def ensure_csv_ends_with_newline(csv_path):
    """
    Ensure that the CSV file ends with a newline character.

    Parameters:
      csv_path (str): Path to the CSV file.
    """
    if not os.path.exists(csv_path):
        return
    with open(csv_path, "rb") as f:
        try:
            f.seek(-1, os.SEEK_END)
        except OSError:
            return  # Empty file.
        last_char = f.read(1)
    if last_char != b"\n":
        with open(csv_path, "a", newline="") as f:
            f.write("\n")
        debug(f"Appended newline to CSV file {csv_path}.")


def sort_csv_alphabetically(csv_path):
    """
    Sort the CSV rows (except the header) alphabetically by algorithm name and iteration number.

    Parameters:
      csv_path (str): Path to the CSV file.
    """
    debug(f"Sorting CSV file {csv_path} alphabetically.")
    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return
    header = rows[0]
    data_rows = [row for row in rows[1:] if row]
    data_rows.sort(key=lambda row: (row[0], int(row[2])))
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data_rows)
    debug(f"Completed sorting CSV file {csv_path}.")


def get_csv_results_for_size(
    size, expected_algs, output_folder="results", max_iterations=None
):
    """
    Retrieve or create a CSV file for a specific array size.

    Parameters:
      size (int): Array size.
      expected_algs (list): List of algorithm names.
      output_folder (str): Folder where CSV files are stored.
      max_iterations (int, optional): Maximum iterations to consider.

    Returns:
      tuple: (csv_path, size_results, max_iters)
    """
    csv_filename = f"results_{size}.csv"
    csv_path = os.path.join(output_folder, csv_filename)
    if os.path.exists(csv_path):
        debug(f"CSV file {csv_path} exists. Reading contents.")
        size_results = read_csv_results(csv_path, expected_algs, max_iterations)
        max_iters = {alg: 0 for alg in expected_algs}  # Placeholder.
    else:
        debug(f"CSV file {csv_path} does not exist. Creating new file with header.")
        os.makedirs(output_folder, exist_ok=True)
        with open(csv_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                ["Algorithm", "Array Size", "Iteration", "Elapsed Time (seconds)"]
            )
        size_results = OrderedDict((alg, None) for alg in expected_algs)
        max_iters = {alg: 0 for alg in expected_algs}
    ensure_csv_ends_with_newline(csv_path)
    return csv_path, size_results, max_iters

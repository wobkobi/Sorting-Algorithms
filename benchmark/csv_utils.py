"""
csv_utils.py

Utility functions for handling CSV files in the benchmark system.

This module provides functions to:
  - Read and parse benchmark results from CSV files.
  - Ensure CSV files end with a newline.
  - Sort CSV rows by algorithm name and iteration number.
  - Retrieve or create CSV files for a given array size.
"""

import csv
import os
from collections import OrderedDict
from benchmark.utils import compute_median, compute_average


def read_csv_results(csv_path, expected_algs):
    """
    Parse benchmark results from a CSV file and compute performance statistics.

    The CSV file is expected to have a header row followed by rows with:
      [Algorithm, Array Size, Iteration, Elapsed Time (seconds)]

    Only valid (float-convertible) elapsed times are used for calculations.

    Parameters:
      csv_path (str): Path to the CSV file.
      expected_algs (list): List of algorithm names expected in the CSV.

    Returns:
      OrderedDict: Mapping from algorithm to a tuple of statistics:
                   (avg, min, max, median, count, times_list)
                   If no valid data exists for an algorithm, its value is None.
    """
    algorithm_times = OrderedDict((alg, []) for alg in expected_algs)

    with open(csv_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        try:
            next(reader)  # Skip header row.
        except StopIteration:
            return algorithm_times  # Empty file; return defaults.

        for row in reader:
            if not row or len(row) < 4:
                continue
            alg = row[0]
            try:
                t = float(row[3])
            except Exception:
                continue
            if alg in algorithm_times:
                algorithm_times[alg].append(t)

    results = OrderedDict()
    for alg in expected_algs:
        times = algorithm_times[alg]
        if times:
            avg = compute_average(times)
            median = compute_median(times)
            results[alg] = (avg, min(times), max(times), median, len(times), times)
        else:
            results[alg] = None

    return results


def ensure_csv_ends_with_newline(csv_path):
    """
    Ensure that the CSV file ends with a newline character.

    This avoids formatting issues when appending new data.

    Parameters:
      csv_path (str): Path to the CSV file.
    """
    if not os.path.exists(csv_path):
        return
    with open(csv_path, "rb") as f:
        try:
            f.seek(-1, os.SEEK_END)
        except OSError:
            return  # File is empty.
        last_char = f.read(1)
    if last_char != b"\n":
        with open(csv_path, "a", newline="") as f:
            f.write("\n")


def sort_csv_alphabetically(csv_path):
    """
    Sort the CSV rows (except the header) alphabetically by algorithm name and iteration number.

    Parameters:
      csv_path (str): Path to the CSV file.
    """
    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return  # Nothing to sort.
    header = rows[0]
    data_rows = [row for row in rows[1:] if row and len(row) > 0]
    data_rows.sort(key=lambda row: (row[0], int(row[2])))
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data_rows)


def get_csv_results_for_size(size, expected_algs, output_folder="results"):
    """
    Retrieve or create a CSV file for a specific array size.

    If the file exists, it parses its contents; otherwise, it creates a new CSV file with the proper header.

    Parameters:
      size (int): Array size used for benchmarking.
      expected_algs (list): List of expected algorithm names.
      output_folder (str): Folder where CSV files are stored.

    Returns:
      tuple: (csv_path, size_results, max_iters)
             - csv_path (str): Full path to the CSV file.
             - size_results (OrderedDict): Parsed benchmark results.
             - max_iters (dict): Mapping from algorithm to the maximum iteration number (currently 0 for all).
    """
    csv_filename = f"results_{size}.csv"
    csv_path = os.path.join(output_folder, csv_filename)
    if os.path.exists(csv_path):
        size_results = read_csv_results(csv_path, expected_algs)
        max_iters = {
            alg: 0 for alg in expected_algs
        }  # Placeholder for iteration count.
    else:
        # Create new CSV file with header.
        with open(csv_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                ["Algorithm", "Array Size", "Iteration", "Elapsed Time (seconds)"]
            )
        size_results = OrderedDict((alg, None) for alg in expected_algs)
        max_iters = {alg: 0 for alg in expected_algs}
    ensure_csv_ends_with_newline(csv_path)
    return csv_path, size_results, max_iters

"""
csv_utils.py

This module provides utility functions for handling CSV files used in the sorting benchmarks.
Functions include:
  - read_csv_results: Read benchmark results from a CSV file and compute statistics.
  - ensure_csv_ends_with_newline: Ensure that a CSV file ends with a newline.
  - sort_csv_alphabetically: Sort the CSV file rows alphabetically based on the first column (Algorithm).
"""

import csv
import os
from collections import OrderedDict
from utils import compute_median, compute_average


def read_csv_results(csv_path, expected_algs):
    """
    Read benchmark results from a CSV file for a specific array size and collect raw timing data.

    The CSV file should have a header and rows formatted as:
      [Algorithm, Array Size, Iteration, Elapsed Time (seconds)]

    For each expected algorithm (provided in expected_algs), this function collects all recorded times
    and then computes:
      - Average elapsed time.
      - Minimum elapsed time.
      - Maximum elapsed time.
      - Median elapsed time.
      - Count of iterations.

    If an algorithm is missing from the CSV, its value is set to None.
    The results are returned in an OrderedDict that preserves the order of expected_algs.

    Parameters:
        csv_path (str): Path to the CSV file.
        expected_algs (list): List of expected algorithm names.

    Returns:
        OrderedDict: Mapping {algorithm: (avg, min, max, median, count, times)} or None if missing.
    """
    # Initialize an ordered dictionary with an empty list for each expected algorithm.
    algorithm_times = OrderedDict((alg, []) for alg in expected_algs)
    with open(csv_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        next(reader)  # Skip header row
        for row in reader:
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
    Ensure that the CSV file at csv_path ends with a newline character.

    This prevents new data from being appended to the last line if the file was not properly terminated.

    Parameters:
        csv_path (str): Path to the CSV file.
    """
    if not os.path.exists(csv_path):
        return
    with open(csv_path, "rb") as f:
        try:
            f.seek(-1, os.SEEK_END)
        except OSError:
            return
        last_char = f.read(1)
    if last_char != b"\n":
        with open(csv_path, "a", newline="") as f:
            f.write("\n")


def sort_csv_alphabetically(csv_path):
    """
    Sort the CSV file at csv_path alphabetically by the first column (Algorithm).

    Reads all rows from the CSV (excluding the header), sorts them based on the first column,
    and then rewrites the CSV file with the header row followed by the sorted data rows.

    Parameters:
        csv_path (str): Path to the CSV file.
    """
    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return
    header = rows[0]
    data_rows = rows[1:]
    data_rows.sort(key=lambda row: row[0])
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data_rows)

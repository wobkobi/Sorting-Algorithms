"""
csv_utils.py

This module provides utility functions for handling CSV files in the benchmark system.
It includes functions to:
  - Read CSV results and compute statistics.
  - Ensure that a CSV file ends with a newline (so new data is appended on a new line).
  - Sort the CSV rows alphabetically by the algorithm name.
"""

import csv
import os
from collections import OrderedDict
from utils import compute_median, compute_average


def read_csv_results(csv_path, expected_algs):
    """
    Read benchmark results from a CSV file for a given array size and collect timing data.

    The CSV file must have a header and rows in the following format:
      [Algorithm, Array Size, Iteration, Elapsed Time (seconds)]

    For each expected algorithm (as listed in expected_algs), all recorded times are collected,
    and the following statistics are computed:
      - Average elapsed time.
      - Minimum elapsed time.
      - Maximum elapsed time.
      - Median elapsed time.
      - Count of iterations.

    If an algorithm is missing from the CSV, its value is set to None.
    Results are returned in an OrderedDict preserving the order given by expected_algs.

    Parameters:
        csv_path (str): Path to the CSV file.
        expected_algs (list): List of expected algorithm names.

    Returns:
        OrderedDict: Mapping {algorithm: (avg, min, max, median, count, times)}
                     or None for algorithms with no data.
    """
    # Initialize an ordered dictionary with an empty list for each expected algorithm.
    algorithm_times = OrderedDict((alg, []) for alg in expected_algs)

    # Open the CSV file.
    with open(csv_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        try:
            header = next(reader)  # Skip header row.
        except StopIteration:
            # CSV file is empty.
            return algorithm_times

        # Process each row.
        for row in reader:
            # Skip empty rows or rows with insufficient columns.
            if not row or len(row) < 4:
                continue
            alg = row[0]
            try:
                t = float(row[3])
            except Exception:
                # Skip rows where the elapsed time cannot be converted.
                continue
            # Only record if the algorithm is expected.
            if alg in algorithm_times:
                algorithm_times[alg].append(t)

    # Compute statistics for each algorithm.
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

    This prevents new rows from being appended to an incomplete final line,
    which could occur if the process stopped abruptly.

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
    Sort the CSV file at csv_path alphabetically based on the first column (Algorithm).

    This function reads all rows (excluding the header), filters out any rows that are empty or
    do not have at least one element, sorts the remaining rows by the algorithm name, and then
    rewrites the CSV file with the header preserved followed by the sorted rows.

    Parameters:
        csv_path (str): Path to the CSV file.
    """
    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)

    # If there are no rows, do nothing.
    if not rows:
        return

    header = rows[0]
    # Filter out any rows that are empty or don't have at least one column.
    data_rows = [row for row in rows[1:] if row and len(row) > 0]
    # Sort rows based on the first column.
    data_rows.sort(key=lambda row: row[0])

    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data_rows)


def get_csv_results_for_size(size, expected_algs, output_folder="results"):
    """
    Retrieve CSV results for a given array size.

    If a CSV file exists for the specified size, read its contents using read_csv_results.
    Otherwise, create a new CSV file with the proper header and return an initial OrderedDict.

    Parameters:
        size (int): The current array size.
        expected_algs (list): List of expected algorithm names.
        output_folder (str): Directory where CSV files are stored.

    Returns:
        tuple: (csv_path, size_results)
    """
    csv_filename = f"results_{size}.csv"
    csv_path = os.path.join(output_folder, csv_filename)
    if os.path.exists(csv_path):
        size_results = read_csv_results(csv_path, expected_algs)
    else:
        with open(csv_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                ["Algorithm", "Array Size", "Iteration", "Elapsed Time (seconds)"]
            )
        size_results = OrderedDict((alg, None) for alg in expected_algs)
    ensure_csv_ends_with_newline(csv_path)
    return csv_path, size_results

"""
This module provides utility functions for handling CSV files used in the benchmark system.

It includes functions to:
  - Read CSV results and compute performance statistics (ignoring DNF iterations).
  - Ensure that the CSV file ends with a newline.
  - Sort CSV rows alphabetically by algorithm name (and iteration number).
  - Retrieve (or create) the CSV file for a given array size.
"""

import csv
import os
from collections import OrderedDict
from utils import compute_median, compute_average


def read_csv_results(csv_path, expected_algs):
    """
    Parse a CSV file containing benchmark results for a given array size and compute statistics.

    The CSV is expected to have rows with the following columns:
      [Algorithm, Array Size, Iteration, Elapsed Time (seconds)]
    - Iteration numbers are converted to integers.
    - The string "DNF" is converted to None.
    - A dictionary is built for each algorithm mapping iteration numbers to their recorded times.
    - Statistics (average, min, max, and median) are computed using only successful runs (non-None values).

    Parameters:
        csv_path (str): Path to the CSV file.
        expected_algs (list): List of algorithm names expected in the results.

    Returns:
        tuple:
          - results (OrderedDict): Maps each algorithm to a tuple:
              (avg, min, max, median, count, times_dict, iter_set)
            where:
              avg       : Average elapsed time for successful iterations (or infinity if none succeeded).
              min, max  : Minimum and maximum elapsed times (or None if no successes).
              median    : Median elapsed time (or None if no successes).
              count     : Total number of iterations recorded.
              times_dict: Dictionary mapping iteration number to its recorded time (None for DNF).
              iter_set  : Set of iteration numbers that were recorded.
          - max_iters (dict): Maps each algorithm to the highest iteration number recorded.
    """
    # Initialize an empty dictionary for each algorithm.
    algorithm_data = {alg: {} for alg in expected_algs}

    # Open the CSV file and parse each row.
    with open(csv_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        try:
            # Skip header row.
            next(reader)
        except StopIteration:
            # Return empty results if the file is empty.
            empty_results = OrderedDict((alg, None) for alg in expected_algs)
            empty_max_iters = {alg: 0 for alg in expected_algs}
            return empty_results, empty_max_iters

        # Process each row.
        for row in reader:
            if not row or len(row) < 4:
                continue
            alg = row[0]
            try:
                iteration = int(row[2])
            except Exception:
                continue
            time_str = row[3].strip()
            # Convert "DNF" to None, otherwise parse the time as a float.
            if time_str == "DNF":
                t = None
            else:
                try:
                    t = float(time_str)
                except Exception:
                    continue
            if alg in algorithm_data:
                algorithm_data[alg][iteration] = t

    # Prepare the results and the maximum iteration numbers for each algorithm.
    results = OrderedDict()
    max_iters = {}
    for alg in expected_algs:
        data = algorithm_data.get(alg, {})
        # The set of iteration numbers recorded.
        iter_set = set(data.keys())
        count = len(iter_set)
        max_iter = max(iter_set) if iter_set else 0
        max_iters[alg] = max_iter
        # Filter out iterations that resulted in DNF (None) for statistics.
        successful_times = [x for x in data.values() if x is not None]
        if successful_times:
            avg = compute_average(successful_times)
            median = compute_median(successful_times)
            results[alg] = (
                avg,
                min(successful_times),
                max(successful_times),
                median,
                count,
                data,
                iter_set,
            )
        else:
            results[alg] = (float("inf"), None, None, None, count, data, iter_set)

    return results, max_iters


def ensure_csv_ends_with_newline(csv_path):
    """
    Ensure the CSV file ends with a newline.

    This function checks the last character of the file. If it is not a newline,
    a newline character is appended to the file.

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
    Sort the CSV file alphabetically by algorithm name and iteration number.

    Reads all rows into memory (excluding the header), sorts them by:
      1. Algorithm name (primary key)
      2. Iteration number (secondary key)
    The sorted rows are then written back to the file.

    Parameters:
        csv_path (str): Path to the CSV file.
    """
    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return
    header = rows[0]
    data_rows = [row for row in rows[1:] if row and len(row) > 0]
    data_rows.sort(key=lambda row: (row[0], int(row[2])))
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data_rows)


def get_csv_results_for_size(size, expected_algs, output_folder="results"):
    """
    Retrieve or create the CSV file for a given array size.

    If a CSV file for the specified size exists, it is parsed using read_csv_results().
    Otherwise, a new CSV file is created with the appropriate header.

    Parameters:
        size (int): The array size being benchmarked.
        expected_algs (list): List of expected algorithm names.
        output_folder (str): Directory where CSV files are stored.

    Returns:
        tuple: (csv_path, size_results, max_iters)
            - csv_path (str): The full path to the CSV file.
            - size_results (OrderedDict): Parsed results from read_csv_results().
            - max_iters (dict): Mapping of algorithm names to the maximum iteration number recorded.
    """
    csv_filename = f"results_{size}.csv"
    csv_path = os.path.join(output_folder, csv_filename)
    if os.path.exists(csv_path):
        size_results, max_iters = read_csv_results(csv_path, expected_algs)
    else:
        with open(csv_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                ["Algorithm", "Array Size", "Iteration", "Elapsed Time (seconds)"]
            )
        size_results = OrderedDict((alg, None) for alg in expected_algs)
        max_iters = {alg: 0 for alg in expected_algs}
    ensure_csv_ends_with_newline(csv_path)
    return csv_path, size_results, max_iters

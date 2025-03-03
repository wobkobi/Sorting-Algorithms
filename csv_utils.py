"""
This module provides utility functions for managing CSV files used in the benchmark system.

It includes functions to:
  - Parse benchmark results from CSV files and compute performance statistics (ignoring DNF iterations).
  - Ensure that CSV files end with a newline.
  - Sort CSV file rows alphabetically by algorithm name and iteration number.
  - Retrieve (or create) the CSV file for a specific array size.
"""

import csv
import os
from collections import OrderedDict
from utils import compute_median, compute_average


def read_csv_results(csv_path, expected_algs):
    """
    Parse benchmark results from a CSV file for a given array size and compute performance statistics.

    The CSV file is expected to contain rows with the following columns:
      [Algorithm, Array Size, Iteration, Elapsed Time (seconds)]
    - Iteration numbers are not used for calculations but are implicitly preserved via the order of entries.
    - The string "DNF" is assumed to be already handled before (or not included in the CSV).
    - All recorded times (as floats) are collected per algorithm; then, statistics (average, min, max, and median)
      are computed using only the successful runs (i.e. non-None values).

    Parameters:
        csv_path (str): The file path to the CSV file.
        expected_algs (list): A list of algorithm names expected in the results.

    Returns:
        OrderedDict: A mapping from each algorithm to a tuple:
            (avg, min, max, median, count, times_list)
        where:
            - avg: Average elapsed time (using only successful iterations; returns infinity if none succeeded)
            - min: Minimum elapsed time (or None if no successful iterations)
            - max: Maximum elapsed time (or None if no successful iterations)
            - median: Median elapsed time (or None if no successful iterations)
            - count: Total number of iterations recorded (including those with DNF, if any)
            - times_list: A list of recorded times (each as a float, or None for a DNF)
    """
    # Initialize a dictionary to hold a list of times for each expected algorithm.
    algorithm_times = OrderedDict((alg, []) for alg in expected_algs)

    with open(csv_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        try:
            # Skip the header row.
            next(reader)
        except StopIteration:
            return algorithm_times  # File is empty

        # Process each row of the CSV.
        for row in reader:
            if not row or len(row) < 4:
                continue
            alg = row[0]
            # Attempt to convert the elapsed time from the row into a float.
            try:
                t = float(row[3])
            except Exception:
                continue
            if alg in algorithm_times:
                algorithm_times[alg].append(t)

    # Compute statistics for each algorithm using only the successful run times.
    results = OrderedDict()
    for alg in expected_algs:
        times = algorithm_times[alg]
        if times:
            avg = compute_average(times)
            median = compute_median(times)
            results[alg] = (avg, min(times), max(times), median, len(times), times)
        else:
            results[alg] = None

    # Clear temporary data.
    del algorithm_times
    return results


def ensure_csv_ends_with_newline(csv_path):
    """
    Check if the CSV file ends with a newline; if not, append a newline.

    This function ensures that the CSV file conforms to standard formatting,
    which can prevent issues when appending new rows.

    Parameters:
        csv_path (str): The file path to the CSV file.
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
    Sort the rows of the CSV file alphabetically by algorithm name and iteration number.

    The function reads the entire CSV file (excluding the header), sorts the data rows by:
      - Primary key: Algorithm name.
      - Secondary key: Iteration number (converted to int).
    The sorted data is then written back to the file.

    Parameters:
        csv_path (str): The file path to the CSV file.
    """
    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return
    header = rows[0]
    # Extract data rows (ignore blank lines) and sort them.
    data_rows = [row for row in rows[1:] if row and len(row) > 0]
    data_rows.sort(key=lambda row: (row[0], int(row[2])))
    # Write the header and sorted rows back to the file.
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data_rows)
    # Clear temporary data.
    del data_rows


def get_csv_results_for_size(size, expected_algs, output_folder="results"):
    """
    Retrieve or create the CSV file for a given array size.

    If a CSV file for the specified array size exists in the output folder,
    its contents are parsed using read_csv_results(). Otherwise, a new CSV file is created
    with a header.

    Parameters:
        size (int): The array size being benchmarked.
        expected_algs (list): A list of expected algorithm names.
        output_folder (str): The directory where CSV files are stored.

    Returns:
        tuple: (csv_path, size_results, max_iters)
            - csv_path (str): The full file path to the CSV file.
            - size_results (OrderedDict): Parsed benchmark results from read_csv_results().
            - max_iters (dict): A mapping from algorithm name to the maximum iteration number recorded.
              (Note: In this basic implementation, max_iters is not computed, so it is set to 0 for all algorithms.)
    """
    csv_filename = f"results_{size}.csv"
    csv_path = os.path.join(output_folder, csv_filename)
    if os.path.exists(csv_path):
        size_results = read_csv_results(csv_path, expected_algs)
        # In this basic version, max_iters is not extracted from the CSV.
        max_iters = {alg: 0 for alg in expected_algs}
    else:
        # Create a new CSV file with the proper header.
        with open(csv_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                ["Algorithm", "Array Size", "Iteration", "Elapsed Time (seconds)"]
            )
        size_results = OrderedDict((alg, None) for alg in expected_algs)
        max_iters = {alg: 0 for alg in expected_algs}
    ensure_csv_ends_with_newline(csv_path)
    return csv_path, size_results, max_iters

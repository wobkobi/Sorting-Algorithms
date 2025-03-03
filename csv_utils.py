"""
csv_utils.py

This module provides utility functions for handling CSV files used in the benchmark system.
It includes functionality to:
  - Read and parse benchmark results from a CSV file.
  - Compute performance statistics (average, min, max, median) for each algorithm.
  - Ensure the CSV file ends with a newline (to support proper appending).
  - Sort CSV rows alphabetically by algorithm name and iteration number.
  - Retrieve (or create) the CSV file for a given array size.

Functions:
    read_csv_results(csv_path, expected_algs)
    ensure_csv_ends_with_newline(csv_path)
    sort_csv_alphabetically(csv_path)
    get_csv_results_for_size(size, expected_algs, output_folder="results")
"""

import csv
import os
from collections import OrderedDict
from utils import compute_median, compute_average


def read_csv_results(csv_path, expected_algs):
    """
    Parse benchmark results from a CSV file for a given array size and compute performance statistics.

    The CSV file should have a header and rows in the following format:
      [Algorithm, Array Size, Iteration, Elapsed Time (seconds)]

    Only successful iterations (where the elapsed time can be converted to float) are used for calculations.

    Parameters:
        csv_path (str): Path to the CSV file.
        expected_algs (list): List of algorithm names that are expected in the CSV.

    Returns:
        OrderedDict: Mapping from each algorithm to a tuple:
            (avg, min, max, median, count, times_list)
        - If no successful iterations exist for an algorithm, its value is None.
    """
    # Initialize dictionary to accumulate times for each algorithm.
    algorithm_times = OrderedDict((alg, []) for alg in expected_algs)

    with open(csv_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        try:
            # Skip the header row.
            next(reader)
        except StopIteration:
            return algorithm_times  # Empty file; return default structure.

        # Process each CSV row.
        for row in reader:
            if not row or len(row) < 4:
                continue  # Skip empty or malformed rows.
            alg = row[0]
            try:
                # Convert the elapsed time to float.
                t = float(row[3])
            except Exception:
                continue  # Skip rows that don't have a valid float time.
            if alg in algorithm_times:
                algorithm_times[alg].append(t)

    # Compute statistics for each algorithm using successful run times.
    results = OrderedDict()
    for alg in expected_algs:
        times = algorithm_times[alg]
        if times:
            avg = compute_average(times)
            median = compute_median(times)
            results[alg] = (avg, min(times), max(times), median, len(times), times)
        else:
            results[alg] = None

    # Clean up temporary data.
    del algorithm_times
    return results


def ensure_csv_ends_with_newline(csv_path):
    """
    Ensure the CSV file ends with a newline character.

    This function checks the last character of the file and appends a newline
    if one is not present. This is useful to prevent formatting issues when appending data.

    Parameters:
        csv_path (str): The file path to the CSV file.
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
    Sort the CSV file rows alphabetically by algorithm name and iteration number.

    Reads the entire CSV file (except the header), sorts the data rows using:
      - Primary key: Algorithm name.
      - Secondary key: Iteration number (converted to integer).
    Writes the header and sorted rows back to the CSV file.

    Parameters:
        csv_path (str): Path to the CSV file.
    """
    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return  # Nothing to sort.
    header = rows[0]
    # Filter out empty rows and sort the remaining rows.
    data_rows = [row for row in rows[1:] if row and len(row) > 0]
    data_rows.sort(key=lambda row: (row[0], int(row[2])))
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data_rows)
    del data_rows  # Clean up temporary list.


def get_csv_results_for_size(size, expected_algs, output_folder="results"):
    """
    Retrieve or create a CSV file for a specific array size.

    If the file exists in the output folder, parse its contents with read_csv_results().
    If it does not exist, create a new file with the proper header.

    Parameters:
        size (int): Array size used in benchmarking.
        expected_algs (list): List of algorithm names expected to be benchmarked.
        output_folder (str): Folder where CSV files are stored.

    Returns:
        tuple: (csv_path, size_results, max_iters)
            - csv_path (str): Full path to the CSV file.
            - size_results (OrderedDict): Parsed benchmark results.
            - max_iters (dict): Mapping from algorithm to the maximum iteration number recorded
              (in this basic implementation, it returns 0 for all algorithms).
    """
    csv_filename = f"results_{size}.csv"
    csv_path = os.path.join(output_folder, csv_filename)
    if os.path.exists(csv_path):
        size_results = read_csv_results(csv_path, expected_algs)
        max_iters = {alg: 0 for alg in expected_algs}  # Placeholder; adjust if needed.
    else:
        # Create a new CSV file with header.
        with open(csv_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(
                ["Algorithm", "Array Size", "Iteration", "Elapsed Time (seconds)"]
            )
        size_results = OrderedDict((alg, None) for alg in expected_algs)
        max_iters = {alg: 0 for alg in expected_algs}
    ensure_csv_ends_with_newline(csv_path)
    return csv_path, size_results, max_iters

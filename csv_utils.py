"""
This module provides utility functions for handling CSV files used in the benchmark system.

It includes functions to:
  - Read CSV results and compute statistics (ignoring DNF iterations).
  - Ensure that a CSV file ends with a newline.
  - Sort the CSV rows alphabetically by algorithm name.
  - Retrieve (or create) the CSV file for a specific array size.
"""

import csv
import os
from collections import OrderedDict
from utils import compute_median, compute_average


def read_csv_results(csv_path, expected_algs):
    """
    Read benchmark results from a CSV file for a given array size and compute statistics.

    Iterates through the CSV file, converting elapsed time values to floats.
    If a row contains "DNF", the result is recorded as None.
    Only successful (non-None) times are used to compute average, min, max, and median.
    The total count of iterations (including DNFs) is preserved.

    Parameters:
        csv_path (str): Path to the CSV file.
        expected_algs (list): List of expected algorithm names.

    Returns:
        OrderedDict: A mapping from algorithm name to a tuple:
            (avg, min, max, median, total_iteration_count, times_list)
            where:
              - avg is the average time of successful runs (or infinity if none succeeded),
              - min, max, and median are computed from successful runs (or None if no successes),
              - total_iteration_count is the total number of iterations recorded,
              - times_list is the list of recorded times (with None representing DNF iterations).
    """
    algorithm_times = OrderedDict((alg, []) for alg in expected_algs)
    with open(csv_path, "r", newline="") as csvfile:
        reader = csv.reader(csvfile)
        try:
            header = next(reader)
        except StopIteration:
            return algorithm_times
        for row in reader:
            if not row or len(row) < 4:
                continue
            alg = row[0]
            time_str = row[3].strip()
            # Record None for "DNF" (Did Not Finish), otherwise try converting to float.
            if time_str == "DNF":
                t = None
            else:
                try:
                    t = float(time_str)
                except Exception:
                    continue
            if alg in algorithm_times:
                algorithm_times[alg].append(t)
    results = OrderedDict()
    for alg in expected_algs:
        times = algorithm_times[alg]
        # Filter out DNFs for computing statistics.
        successful_times = [x for x in times if x is not None]
        if successful_times:
            avg = compute_average(successful_times)
            median = compute_median(successful_times)
            results[alg] = (
                avg,
                min(successful_times),
                max(successful_times),
                median,
                len(times),
                times,
            )
        else:
            # If no successful runs, set avg to infinity and other statistics to None.
            results[alg] = (float("inf"), None, None, None, len(times), times)
    return results


def ensure_csv_ends_with_newline(csv_path):
    """
    Ensure that the CSV file at 'csv_path' ends with a newline character.

    If the file does not exist or is empty, the function does nothing.
    Otherwise, it appends a newline if the last character is not a newline.

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
    Sort the CSV file at 'csv_path' alphabetically based on the first column (Algorithm name).

    Reads the CSV file into memory, sorts the data rows (ignoring the header) by the algorithm name
    (and iteration number as a secondary key), and writes the sorted data back to the file.

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
    Retrieve or create a CSV file for the specified array size.

    If a CSV file for the given size exists in the output folder, its contents are read
    and parsed using read_csv_results(). Otherwise, a new CSV file is created with the proper header.

    Parameters:
        size (int): The current array size.
        expected_algs (list): List of expected algorithm names.
        output_folder (str): Directory where CSV files are stored.

    Returns:
        tuple: (csv_path, size_results)
            - csv_path: Path to the CSV file.
            - size_results: Parsed results (an OrderedDict) obtained by calling read_csv_results().
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

"""
csv_utils.py

This module provides utility functions for handling CSV files in the benchmark system.
It includes functions to:
  - Read CSV results and compute statistics.
  - Ensure that a CSV file ends with a newline.
  - Sort the CSV rows alphabetically by the algorithm name.
"""

import csv
import os
from collections import OrderedDict
from utils import compute_median, compute_average


def read_csv_results(csv_path, expected_algs):
    """
    Read benchmark results from a CSV file for a given array size and collect timing data.
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
    del algorithm_times  # Clear temporary data
    return results


def ensure_csv_ends_with_newline(csv_path):
    """
    Ensure that the CSV file at csv_path ends with a newline character.
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
    """
    with open(csv_path, "r", newline="") as f:
        reader = csv.reader(f)
        rows = list(reader)
    if not rows:
        return
    header = rows[0]
    data_rows = [row for row in rows[1:] if row and len(row) > 0]
    data_rows.sort(key=lambda row: (row[0], int(row[2])))
    del rows  # Clear the full list after processing
    with open(csv_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(data_rows)
    del data_rows  # Clear temporary list


def get_csv_results_for_size(size, expected_algs, output_folder="results"):
    """
    Retrieve CSV results for a given array size.
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

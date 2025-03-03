"""
utils.py

This module provides helper functions used throughout the benchmark application.
It includes functions for:
  - Formatting time durations into human-readable strings.
  - Grouping algorithms into performance clusters.
  - Running a single benchmark iteration.
  - Computing average and median values.
  - Converting integers to ordinal string representations.
  
Functions:
    format_time(seconds, detailed=False)
    group_rankings(ranking, margin=1e-3)
    run_iteration(sort_func, size)
    compute_average(times)
    compute_median(times)
    ordinal(n)
"""

import math
import time
import random


def format_time(seconds, detailed=False):
    """
    Format a time duration (in seconds) into a human-readable string.

    For very short durations, different levels of detail are shown based on the 'detailed' flag.

    Examples:
      - For durations < 0.001 s:
          * Detailed: "123us"
          * Non-detailed: "less than a ms"
      - For durations < 1 s: Displays in milliseconds.
      - For durations between 1 and 60 s: Displays seconds and milliseconds.
      - For durations between 60 s and 1 hr: Displays minutes, seconds, and milliseconds.
      - For durations >= 1 hr: Displays hours, minutes, and seconds.

    Parameters:
        seconds (float): Duration in seconds.
        detailed (bool): Flag to enable extra precision for very short durations.

    Returns:
        str: Formatted time string.
    """
    if seconds is None or (isinstance(seconds, float) and math.isnan(seconds)):
        return "NaN"
    if seconds < 1e-3:
        if detailed:
            us = int(round(seconds * 1e6))
            return f"{us}us"
        else:
            return "less than a ms"
    elif seconds < 1:
        total_us = int(round(seconds * 1e6))
        ms = total_us // 1000
        remainder_us = total_us % 1000
        if detailed and remainder_us:
            return f"{ms}ms {remainder_us}us"
        else:
            return f"{ms}ms"
    elif seconds < 60:
        sec = int(seconds)
        ms = int(round((seconds - sec) * 1000))
        return f"{sec}s {ms}ms"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        sec = int(seconds % 60)
        ms = int(round((seconds - minutes * 60 - sec) * 1000))
        return f"{minutes}min {sec}s {ms}ms"
    else:
        hr = int(seconds // 3600)
        rem = seconds % 3600
        minutes = int(rem // 60)
        sec = int(rem % 60)
        return f"{hr}hr {minutes}min {sec}s"


def group_rankings(ranking, margin=1e-3):
    """
    Group a sorted list of (algorithm, average_time) tuples that are within a specified margin.

    This function clusters algorithms with similar performance into groups.

    Parameters:
        ranking (list): Sorted list of tuples in the form (algorithm, average_time).
        margin (float): Maximum difference between consecutive times to consider them tied.

    Returns:
        list: A list of groups (each group is a list of tuples).
    """
    if not ranking:
        return []
    groups = []
    current_group = [ranking[0]]
    for item in ranking[1:]:
        if item[1] - current_group[-1][1] < margin:
            current_group.append(item)
        else:
            groups.append(current_group)
            current_group = [item]
    groups.append(current_group)
    return groups


def run_iteration(sort_func, size):
    """
    Run a single benchmark iteration of a sorting algorithm.

    Generates a random array of integers of the given size, sorts a copy using the provided function,
    and returns the elapsed time.

    Parameters:
        sort_func (callable): The sorting algorithm to run.
        size (int): Size of the array to sort.

    Returns:
        float: Elapsed time in seconds.
    """
    arr = [random.randint(-1000000, 1000000) for _ in range(size)]
    start = time.perf_counter()
    sort_func(arr.copy())
    return time.perf_counter() - start


def compute_average(times):
    """
    Compute the arithmetic mean of a list of numbers.

    Parameters:
        times (list): List of numerical values.

    Returns:
        float or None: Average value or None if the list is empty.
    """
    if times:
        return sum(times) / len(times)
    return None


def compute_median(times):
    """
    Compute the median value from a list of numbers.

    For even counts, returns the average of the two central values.

    Parameters:
        times (list): List of numerical values.

    Returns:
        float or None: Median value or None if the list is empty.
    """
    n = len(times)
    if n == 0:
        return None
    sorted_times = sorted(times)
    if n % 2 == 0:
        return (sorted_times[n // 2 - 1] + sorted_times[n // 2]) / 2
    return sorted_times[n // 2]


def ordinal(n):
    """
    Convert an integer to its ordinal string representation.

    Examples:
        1 -> "1st", 2 -> "2nd", 3 -> "3rd", 4 -> "4th"

    Parameters:
        n (int): The integer value.

    Returns:
        str: Ordinal string.
    """
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

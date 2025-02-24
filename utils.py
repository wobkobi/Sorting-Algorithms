"""
utils.py

This module provides helper functions for:
  - Formatting time durations.
  - Grouping ranking results based on performance similarity.
  - Running individual benchmark iterations.
  - Computing average and median values.
"""

import time
import random


def format_time(seconds):
    """
    Convert a duration in seconds to a human-readable string with abbreviated time units.

    Formats:
      - "less than a ms" if duration < 0.001 s.
      - For durations < 1 s: e.g. "123ms".
      - For 1–60 s: e.g. "3s 120ms".
      - For 60 s–1 hr: e.g. "2min 3s 120ms".
      - For >= 1 hr: e.g. "1hr 2min 3s".

    Parameters:
        seconds (float): Duration in seconds.

    Returns:
        str: Formatted time string.
    """
    if seconds < 1e-3:
        return "less than a ms"
    elif seconds < 1:
        ms = int(round(seconds * 1000))
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
    Group a sorted list of (algorithm, average time) tuples whose consecutive times differ by less than a margin.

    This is used to group algorithms with similar performance.

    Parameters:
        ranking (list of tuple): Sorted list in the form (algorithm, average_time).
        margin (float): Maximum allowed difference between consecutive times for grouping.

    Returns:
        list of list: A list of groups, where each group is a list of (algorithm, average_time) tuples.
    """
    groups = []
    if not ranking:
        return groups
    current = [ranking[0]]
    for item in ranking[1:]:
        if item[1] - current[-1][1] < margin:
            current.append(item)
        else:
            groups.append(current)
            current = [item]
    groups.append(current)
    return groups


def run_iteration(sort_func, size):
    """
    Execute one iteration of a sorting algorithm on a randomly generated integer array and measure its runtime.

    Generates a random array of integers, sorts a copy using the provided sort function,
    and returns the elapsed time.

    Parameters:
        sort_func (function): The sorting function to execute.
        size (int): The size of the array.

    Returns:
        float: Elapsed time in seconds.
    """
    arr = [random.randint(-1000000, 1000000) for _ in range(size)]
    start = time.perf_counter()
    sort_func(arr.copy())
    return time.perf_counter() - start


def compute_average(times):
    """
    Calculate the average value from a list of numbers.

    Parameters:
        times (list of float): List of numerical values (e.g., execution times).

    Returns:
        float or None: The average value, or None if the list is empty.
    """
    return sum(times) / len(times) if times else None


def compute_median(times):
    """
    Compute the median value from a list of numbers.

    For an even number of elements, returns the average of the two middle values.

    Parameters:
        times (list of float): List of numerical values.

    Returns:
        float or None: The median value, or None if the list is empty.
    """
    n = len(times)
    if n == 0:
        return None
    sorted_times = sorted(times)
    if n % 2 == 0:
        return (sorted_times[n // 2 - 1] + sorted_times[n // 2]) / 2
    return sorted_times[n // 2]

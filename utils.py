"""
utils.py

This module provides helper functions for:
  - Converting time durations into human-readable strings.
  - Grouping ranking results based on performance similarity.
  - Running a single benchmark iteration.
  - Calculating average and median values from a list of times.
"""

import time
import random


def format_time(seconds):
    """
    Convert a duration in seconds to a human-readable string with abbreviated time units.

    Examples:
      - "less than a ms" if duration < 0.001 s.
      - "123ms" if duration < 1 s.
      - "3s 120ms" for durations between 1 and 60 s.
      - "2min 3s 120ms" for durations between 60 s and 1 hr.
      - "1hr 2min 3s" for durations >= 1 hr.

    Parameters:
        seconds (float): Duration in seconds.

    Returns:
        str: The formatted time string.
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
    Group a sorted list of (algorithm, average time) tuples whose consecutive times differ by less than a given margin.

    This is used to cluster algorithms with similar performance metrics.

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

    A random array of integers is generated and a copy is sorted using the provided sorting function.
    The elapsed time for the sort is returned.

    Parameters:
        sort_func (function): The sorting function to execute.
        size (int): The size of the array.

    Returns:
        float: The elapsed time in seconds.
    """
    arr = [random.randint(-1000000, 1000000) for _ in range(size)]
    start = time.perf_counter()
    sort_func(arr.copy())
    return time.perf_counter() - start


def compute_average(times):
    """
    Calculate the average of a list of numbers.

    Parameters:
        times (list of float): A list of execution times.

    Returns:
        float or None: The average value, or None if the list is empty.
    """
    return sum(times) / len(times) if times else None


def compute_median(times):
    """
    Compute the median value from a list of numbers.

    For an even number of elements, returns the average of the two middle values.

    Parameters:
        times (list of float): A list of execution times.

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

"""
utils.py

Helper functions for the benchmark application.
Provides functions for formatting time, grouping rankings,
running a benchmark iteration, and calculating statistical values.
"""

import math
import time
import random
from .config import debug


def format_time(seconds, detailed=False):
    """
    Format a time duration (in seconds) into a human-readable string.

    Parameters:
      seconds (number): The time duration in seconds.
      detailed (bool): If True, provides extra precision for very short durations.

    Returns:
      str: The formatted time or "NaN" for invalid input.
    """
    try:
        seconds = float(seconds)
    except (ValueError, TypeError):
        return "NaN"
    if seconds is None or math.isnan(seconds):
        return "NaN"
    try:
        if seconds < 1e-3:
            return f"{int(round(seconds * 1e6))}us" if detailed else "less than a ms"
        elif seconds < 1:
            total_us = int(round(seconds * 1e6))
            ms = total_us // 1000
            remainder_us = total_us % 1000
            return (
                f"{ms}ms {remainder_us}us" if detailed and remainder_us else f"{ms}ms"
            )
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
    except Exception:
        return "NaN"


def group_rankings(ranking, margin=1e-3):
    """
    Group algorithms into clusters based on similar average times.

    Parameters:
      ranking (list): Sorted list of tuples (algorithm, average_time, ...).
      margin (float): Maximum allowed difference to group times together.

    Returns:
      list: List of grouped rankings.
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
    Execute a single iteration of a sorting algorithm benchmark.

    Generates a random array of given size, runs the sort function,
    and returns the elapsed time.

    Parameters:
      sort_func (callable): The sorting function to test.
      size (int): The size of the array.

    Returns:
      float: Elapsed time in seconds.
    """

    debug(f"Starting iteration for {sort_func.__name__} on array size {size}.")
    arr = [random.randint(-1000000, 1000000) for _ in range(size)]
    start = time.perf_counter()
    sort_func(arr.copy())
    elapsed = time.perf_counter() - start
    debug(
        f"Completed iteration for {sort_func.__name__} on array size {size} in {elapsed:.8f} seconds."
    )
    return elapsed


def compute_average(times):
    """
    Compute the average of a list of numbers.

    Parameters:
      times (list): List of numerical values.

    Returns:
      float or None: The average value, or None if the list is empty.
    """
    return sum(times) / len(times) if times else None


def compute_median(times):
    """
    Compute the median of a list of numbers.

    Parameters:
      times (list): List of numerical values.

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


def compute_variance(avg, mn, mx):
    """
    Compute the variance percentage defined as ((max - min) / avg) * 100.

    Parameters:
      avg (float): The average time.
      mn (float): Minimum time.
      mx (float): Maximum time.

    Returns:
      float or None: The variance percentage, or None if avg is zero.
    """
    if avg is None or avg == 0:
        return None
    return ((mx - mn) / avg) * 100


def ordinal(n):
    """
    Convert an integer n to its ordinal string representation (e.g., 1 -> '1st').

    Parameters:
      n (int): The integer.

    Returns:
      str: The ordinal string.
    """
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def format_size(size):
    """
    Format an integer size by inserting commas as thousand separators if necessary.

    Parameters:
      size (int): The size number.

    Returns:
      str: The formatted size.
    """
    return f"{size:,}" if size >= 10000 else str(size)

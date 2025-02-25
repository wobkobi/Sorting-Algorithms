"""
This module provides helper functions for common operations used in the benchmark.

It includes functions for:
- Converting time durations into human-readable strings.
- Grouping ranking results based on performance similarity.
- Running a single benchmark iteration.
- Calculating average and median values from a list of times.
- Converting integers to their ordinal string representation.
"""

import time
import random


def format_time(seconds, detailed=False):
    """
    Convert a duration in seconds to a human-readable string with abbreviated time units.

    Depending on the value of 'detailed', very short durations are displayed with additional precision.

    Examples:
      - If seconds < 0.001 and detailed is False, returns "less than a ms".
      - If seconds < 0.001 and detailed is True, returns the time in microseconds (e.g., "123us").
      - For durations < 1 s, returns the time in milliseconds (e.g., "123ms").
      - For durations between 1 and 60 s, returns seconds and milliseconds (e.g., "3s 120ms").
      - For durations between 60 s and 1 hr, returns minutes, seconds, and milliseconds (e.g., "2min 3s 120ms").
      - For durations >= 1 hr, returns hours, minutes, and seconds (e.g., "1hr 2min 3s").

    Parameters:
        seconds (float): The duration in seconds.
        detailed (bool): If True, show sub-millisecond details (microseconds) for very short durations.

    Returns:
        str: A formatted string representing the duration.
    """
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
    Group a sorted list of (algorithm, average time) tuples whose consecutive times differ
    by less than a given margin. This clusters algorithms with similar performance.

    Parameters:
        ranking (list): A sorted list of tuples in the form (algorithm, average_time).
        margin (float): Maximum allowed difference between consecutive times to be considered tied.

    Returns:
        list: A list of groups, where each group is a list of (algorithm, average time) tuples.
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
    Execute one iteration of a sorting algorithm on a randomly generated integer array and measure its runtime.

    Parameters:
        sort_func (callable): The sorting function to execute.
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
    Compute the average of a list of numbers.

    Parameters:
        times (list): A list of numerical values (e.g., execution times).

    Returns:
        float or None: The average of the values, or None if the list is empty.
    """
    if times:
        return sum(times) / len(times)
    return None


def compute_median(times):
    """
    Compute the median value from a list of numbers.

    For an even number of elements, returns the average of the two middle values.

    Parameters:
        times (list): A list of numerical values (e.g., execution times).

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


def ordinal(n):
    """
    Convert an integer to its ordinal string representation.

    For example:
      - 1 becomes "1st"
      - 2 becomes "2nd"
      - 3 becomes "3rd"
      - 4 becomes "4th"

    Parameters:
        n (int): The integer to convert.

    Returns:
        str: The ordinal string representation of the integer.
    """
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

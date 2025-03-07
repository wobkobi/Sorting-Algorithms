"""
utils.py

Helper functions for the benchmark application.

Functions include:
  - Time formatting (format_time).
  - Grouping algorithm rankings (group_rankings).
  - Running a single benchmark iteration (run_iteration).
  - Calculating average and median values.
  - Converting integers to ordinal strings.
"""

import math
import time
import random


def format_time(seconds, detailed=False):
    """
    Format a time duration (in seconds) into a human-readable string.

    If seconds is NaN, None, or an invalid number, returns "NaN".

    For valid numbers:
      - For durations < 1ms, returns microseconds (if detailed) or "less than a ms".
      - For durations < 1s, returns milliseconds.
      - For durations < 60s, returns seconds and milliseconds.
      - For durations < 3600s, returns minutes, seconds, and milliseconds.
      - Otherwise, returns hours, minutes, and seconds.

    Parameters:
      seconds (number): Duration in seconds.
      detailed (bool): If True, shows extra precision for very short durations.

    Returns:
      str: The formatted time string, or "NaN" if the input is invalid.
    """
    try:
        seconds = float(seconds)
    except (ValueError, TypeError):
        return "NaN"

    # Check for NaN or None
    if seconds is None or math.isnan(seconds):
        return "NaN"

    try:
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
    except Exception:
        # In case any unexpected arithmetic error occurs, return "NaN"
        return "NaN"


def group_rankings(ranking, margin=1e-3):
    """
    Group algorithms into clusters based on similar performance.

    Algorithms are grouped together if their average times differ by less than the given margin.

    Parameters:
      ranking (list): Sorted list of tuples (algorithm, average_time).
      margin (float): Maximum difference to consider times as tied.

    Returns:
      list: A list of groups, where each group is a list of tuples.
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

    Generates a random array of the given size, then times how long the sorting function takes.

    Parameters:
      sort_func (callable): The sorting function to test.
      size (int): The size of the array to generate.

    Returns:
      float: Elapsed time in seconds.
    """
    arr = [random.randint(-1000000, 1000000) for _ in range(size)]
    start = time.perf_counter()
    sort_func(arr.copy())
    return time.perf_counter() - start


def compute_average(times):
    """
    Calculate the average of a list of numbers.

    Parameters:
      times (list): List of numerical values.

    Returns:
      float or None: The average value, or None if the list is empty.
    """
    if times:
        return sum(times) / len(times)
    return None


def compute_median(times):
    """
    Compute the median value from a list of numbers.

    For even-numbered lists, returns the average of the two middle values.

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


def ordinal(n):
    """
    Convert an integer to its ordinal string representation.

    Examples:
      1 -> "1st", 2 -> "2nd", 3 -> "3rd", 4 -> "4th", etc.

    Parameters:
      n (int): The integer to convert.

    Returns:
      str: The ordinal representation.
    """
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"


def format_size(size):
    """
    Format an integer size by inserting commas as thousand separators for values 10,000 and above.

    If the size is less than 10,000, the function returns it as a string without commas.

    Parameters:
      size (int): The integer to format.

    Returns:
      str: The formatted string.
    """
    if size >= 10000:
        return f"{size:,}"
    return str(size)

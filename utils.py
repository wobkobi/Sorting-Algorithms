"""
utils.py

This module provides helper functions for:
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
      - seconds: The duration in seconds.
      - detailed: If True, show sub-millisecond details (microseconds) for very short durations.

    Returns:
      A formatted string representing the duration.
    """
    # For durations shorter than 1 millisecond.
    if seconds < 1e-3:
        if detailed:
            # Calculate microseconds and return as e.g. "123us"
            us = int(round(seconds * 1e6))
            return f"{us}us"
        else:
            return "less than a ms"
    # For durations between 1 millisecond and 1 second.
    elif seconds < 1:
        total_us = int(round(seconds * 1e6))
        ms = total_us // 1000
        remainder_us = total_us % 1000
        # If detailed mode is on and there is a remainder, include microseconds.
        if detailed and remainder_us:
            return f"{ms}ms {remainder_us}us"
        else:
            return f"{ms}ms"
    # For durations between 1 second and 1 minute.
    elif seconds < 60:
        sec = int(seconds)
        ms = int(round((seconds - sec) * 1000))
        return f"{sec}s {ms}ms"
    # For durations between 1 minute and 1 hour.
    elif seconds < 3600:
        minutes = int(seconds // 60)
        sec = int(seconds % 60)
        ms = int(round((seconds - minutes * 60 - sec) * 1000))
        return f"{minutes}min {sec}s {ms}ms"
    # For durations of 1 hour or more.
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

    It is assumed that the input 'ranking' list is already sorted by average time.

    Parameters:
      - ranking: A sorted list of tuples in the form (algorithm, average_time).
      - margin: The maximum allowed difference between consecutive times to be considered tied.

    Returns:
      A list of groups, where each group is a list of (algorithm, average time) tuples.
    """
    if not ranking:
        return []

    groups = []
    # Start with the first tuple in the current group.
    current_group = [ranking[0]]

    # Iterate over the remaining items.
    for item in ranking[1:]:
        # If the difference between the current item's average time and the last in the group is within the margin,
        # add it to the current group.
        if item[1] - current_group[-1][1] < margin:
            current_group.append(item)
        else:
            groups.append(current_group)
            current_group = [item]

    # Append the last group.
    groups.append(current_group)
    return groups


def run_iteration(sort_func, size):
    """
    Execute one iteration of a sorting algorithm on a randomly generated integer array and measure its runtime.

    Generates a random array of integers of the specified size, sorts a copy of the array using the provided
    sorting function, and returns the elapsed time.

    Parameters:
      - sort_func: The sorting function to be executed.
      - size: The size of the array.

    Returns:
      The elapsed time in seconds.
    """
    # Create an array of random integers.
    arr = [random.randint(-1000000, 1000000) for _ in range(size)]
    start = time.perf_counter()
    sort_func(arr.copy())
    return time.perf_counter() - start


def compute_average(times):
    """
    Compute the average of a list of numbers.

    Parameters:
      - times: A list of numerical values (e.g., execution times).

    Returns:
      The average of the values, or None if the list is empty.
    """
    if times:
        return sum(times) / len(times)
    return None


def compute_median(times):
    """
    Compute the median value from a list of numbers.

    For an even number of elements, returns the average of the two middle values.

    Parameters:
      - times: A list of numerical values (e.g., execution times).

    Returns:
      The median value, or None if the list is empty.
    """
    n = len(times)
    if n == 0:
        return None
    sorted_times = sorted(times)
    # If even, return the average of the two middle numbers.
    if n % 2 == 0:
        return (sorted_times[n // 2 - 1] + sorted_times[n // 2]) / 2
    # If odd, return the middle element.
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
      - n: The integer to convert.

    Returns:
      The ordinal string representation of the integer.
    """
    # Numbers between 10 and 20 (inclusive) always use "th"
    if 10 <= n % 100 <= 20:
        suffix = "th"
    else:
        # Otherwise, use the last digit to determine the suffix.
        suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
    return f"{n}{suffix}"

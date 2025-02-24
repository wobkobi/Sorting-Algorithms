import time
import random


def format_time(seconds):
    """
    Convert a duration in seconds to a human-readable string with abbreviated time units.

    The format is as follows:
      - "less than a ms" if the duration is less than 0.001 seconds.
      - For durations < 1 second: e.g. "123ms".
      - For durations between 1 and 60 seconds: e.g. "3s 120ms".
      - For durations between 60 seconds and 1 hour: e.g. "2min 3s 120ms".
      - For durations of 1 hour or more: e.g. "1hr 2min 3s".

    Parameters:
        seconds (float): The duration in seconds.

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
    Group a sorted list of (algorithm, time) tuples where consecutive entries differ by less than a specified margin.

    This function is used to group algorithms that have nearly identical performance metrics.

    Parameters:
        ranking (list of tuple): A sorted list of tuples in the form (algorithm, avg_time).
        margin (float): The maximum allowed difference (in seconds) between consecutive times to be grouped together.

    Returns:
        list of list: A list of groups, where each group is a list of (algorithm, avg_time) tuples.
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

    The function generates an array of random integers of the specified size, runs the provided sorting
    function on a copy of the array, and returns the elapsed time.

    Parameters:
        sort_func (function): The sorting function to be executed.
        size (int): The size of the randomly generated integer array.

    Returns:
        float: The elapsed time in seconds for the sorting operation.
    """
    arr = [random.randint(-1000000, 1000000) for _ in range(size)]
    start = time.perf_counter()
    sort_func(arr.copy())
    return time.perf_counter() - start


def compute_average(times):
    """
    Calculate the average of a list of numerical values.

    Parameters:
        times (list of float): A list of numerical values (e.g., execution times).

    Returns:
        float or None: The average of the values, or None if the list is empty.
    """
    return sum(times) / len(times) if times else None


def compute_median(times):
    """
    Compute the median value from a list of numbers.

    The function returns the median, which is the middle value in the sorted list. If the list has an even number
    of elements, the median is calculated as the average of the two middle values.

    Parameters:
        times (list of float): A list of numbers (e.g., execution times).

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

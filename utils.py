import time
import random


def format_time(seconds):
    """
    Convert seconds into a human-readable string using abbreviated units (ms, s, min, hr)
    with no space between the number and the unit.

    - "less than a ms" if time < 0.001 seconds.
    - For time < 1 second: e.g., "123ms".
    - For time between 1 and 60 seconds: e.g., "3s120ms".
    - For time between 60 seconds and 1 hour: e.g., "2min3s120ms".
    - For time >= 1 hour: e.g., "1hr2min3s".

    Parameters:
        seconds (float): Time duration in seconds.

    Returns:
        str: Formatted time string.
    """
    if seconds < 1e-3:
        return "less than a ms"
    elif seconds < 1:
        ms = int(round(seconds * 1000))
        return f"{ms}ms"
    elif seconds < 60:
        sec_int = int(seconds)
        ms = int(round((seconds - sec_int) * 1000))
        return f"{sec_int}s {ms}ms"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        rem = seconds % 60
        sec_int = int(rem)
        ms = int(round((rem - sec_int) * 1000))
        return f"{minutes}min {sec_int}s {ms}ms"
    else:
        hours = int(seconds // 3600)
        rem = seconds % 3600
        minutes = int(rem // 60)
        sec_int = int(rem % 60)
        return f"{hours}hr {minutes}min {sec_int}s"


def group_rankings(ranking, margin=1e-3):
    """
    Group a sorted list of (algorithm, avg_time) tuples if the difference between consecutive values is below margin.

    Parameters:
        ranking (list): Sorted list of tuples (algorithm, avg_time).
        margin (float): Maximum allowed difference (in seconds) for grouping.

    Returns:
        list: A list of groups, each a list of (algorithm, avg_time) tuples.
    """
    groups = []
    if not ranking:
        return groups
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
    Run one iteration of a sorting function on a random integer array.

    Parameters:
        sort_func (function): Sorting algorithm to benchmark.
        size (int): Size of the array.

    Returns:
        float: Elapsed time in seconds.
    """
    arr = [random.randint(-1000000, 1000000) for _ in range(size)]
    start = time.perf_counter()
    sort_func(arr.copy())
    return time.perf_counter() - start


def compute_average(times):
    """
    Compute the average of a list of numbers.

    Parameters:
        times (list): List of numerical values.

    Returns:
        float or None: Average value, or None if empty.
    """
    return sum(times) / len(times) if times else None

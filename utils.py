import time
import random


def format_time(seconds):
    """
    Convert seconds into a human-readable string using abbreviated units with no space between number and unit.

    - "less than a ms" if < 0.001 s.
    - For < 1 s: e.g. "123ms".
    - For 1–60 s: e.g. "3s120ms".
    - For 60 s–1 hr: e.g. "2min3s120ms".
    - For >= 1 hr: e.g. "1hr2min3s".

    Parameters:
        seconds (float): Duration in seconds.
    Returns:
        str: Formatted time.
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
    Group sorted (algorithm, avg_time) tuples if consecutive differences are less than margin.

    Parameters:
        ranking (list): Sorted list of (algorithm, avg_time).
        margin (float): Maximum difference (seconds) for grouping.

    Returns:
        list: List of groups.
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
    Run one iteration of a sorting function on a random integer array.

    Parameters:
        sort_func (function): Sorting algorithm.
        size (int): Array size.

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
        times (list): List of numbers.

    Returns:
        float or None: Average, or None if list empty.
    """
    return sum(times) / len(times) if times else None

import time
import random


def format_time(seconds):
    """
    Convert a time in seconds into a human-readable string using abbreviated units,
    with no space between the number and the unit.

    Returns:
      - "less than 1ms" if time is below 0.001 seconds.
      - For times < 1 second, displays time in milliseconds (e.g., "123ms").
      - For times between 1 and 60 seconds, displays seconds and milliseconds (e.g., "3s120ms").
      - For times between 60 seconds and 1 hour, displays minutes, seconds, and milliseconds (e.g., "2min3s120ms").
      - For times 1 hour or more, displays hours, minutes, and seconds (e.g., "1hr2min3s").

    Parameters:
        seconds (float): Time duration in seconds.

    Returns:
        str: The formatted time string.
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
    Group a sorted list of (algorithm, avg_time) tuples if the difference between
    consecutive average times is less than the specified margin.

    Parameters:
        ranking (list): Sorted list of tuples in the form (algorithm, avg_time).
        margin (float): Maximum allowed difference in seconds for grouping.

    Returns:
        list: A list of groups, where each group is a list of (algorithm, avg_time) tuples.
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
    Execute a single iteration of the provided sort function on a randomly generated array.

    Parameters:
        sort_func (function): The sorting algorithm function to be benchmarked.
        size (int): The size (length) of the array to be sorted.

    Returns:
        float: The elapsed time in seconds.
    """
    arr = [random.randint(-1000000, 1000000) for _ in range(size)]
    arr_copy = arr.copy()
    start_time = time.perf_counter()
    sort_func(arr_copy)
    return time.perf_counter() - start_time

import time
import random


def format_time(seconds):
    """
    Convert a time in seconds into a human-readable string with full integer rounding.

    - If time is less than 1 millisecond, returns "less than 1 millisecond".
    - For times < 1 second, displays milliseconds (rounded to whole numbers).
    - For times between 1 and 60 seconds, displays seconds and milliseconds.
    - For times between 60 seconds and 1 hour, displays minutes, seconds, and milliseconds.
    - For times >= 1 hour, displays hours, minutes, and seconds.
    """
    if seconds < 1e-3:
        return "less than 1 millisecond"
    elif seconds < 1:
        ms = int(round(seconds * 1000))
        return f"{ms} millisecond{'s' if ms != 1 else ''}"
    elif seconds < 60:
        sec_int = int(seconds)
        ms = int(round((seconds - sec_int) * 1000))
        return f"{sec_int} second{'s' if sec_int != 1 else ''} and {ms} millisecond{'s' if ms != 1 else ''}"
    elif seconds < 3600:
        minutes = int(seconds // 60)
        rem = seconds % 60
        sec_int = int(rem)
        ms = int(round((rem - sec_int) * 1000))
        return f"{minutes} minute{'s' if minutes != 1 else ''}, {sec_int} second{'s' if sec_int != 1 else ''} and {ms} millisecond{'s' if ms != 1 else ''}"
    else:
        hours = int(seconds // 3600)
        rem = seconds % 3600
        minutes = int(rem // 60)
        sec_int = int(rem % 60)
        return f"{hours} hour{'s' if hours != 1 else ''}, {minutes} minute{'s' if minutes != 1 else ''} and {sec_int} second{'s' if sec_int != 1 else ''}"


def group_rankings(ranking, margin=1e-3):
    """
    Group a sorted list of (algorithm, avg_time) tuples if their average times differ by less than the margin.

    Parameters:
        ranking (list): Sorted list of (algorithm, avg_time) tuples.
        margin (float): Threshold in seconds.

    Returns:
        List of groups (each group is a list of (algorithm, avg_time) tuples).
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
    Run a single iteration of a sort function for a given input size.

    Parameters:
        sort_func (function): The sorting algorithm to benchmark.
        size (int): The size of the input array.

    Returns:
        float: Elapsed time in seconds.
    """
    arr = [random.randint(-1000000, 1000000) for _ in range(size)]
    arr_copy = arr.copy()
    start_time = time.perf_counter()
    sort_func(arr_copy)
    return time.perf_counter() - start_time

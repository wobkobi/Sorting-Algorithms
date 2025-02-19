import time
import random


def format_time(seconds):
    """
    Convert a given time in seconds into a human-readable string, rounding values to whole numbers.

    Returns:
      - "less than 1 millisecond" if the time is below 0.001 seconds.
      - Milliseconds if the time is below 1 second.
      - Seconds and milliseconds if the time is between 1 and 60 seconds.
      - Minutes, seconds, and milliseconds if the time is between 60 seconds and 1 hour.
      - Hours, minutes, and seconds if the time is 1 hour or more.

    Parameters:
        seconds (float): Time duration in seconds.

    Returns:
        str: Formatted time string.
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
    Group a sorted list of (algorithm, average time) tuples if the difference between
    consecutive average times is less than the specified margin.

    Parameters:
        ranking (list): A sorted list of tuples in the form (algorithm, avg_time).
        margin (float): The maximum difference (in seconds) allowed for values to be grouped.

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
        float: The elapsed time in seconds to perform the sort.
    """
    # Create an array of the specified size with random integers.
    arr = [random.randint(-1000000, 1000000) for _ in range(size)]
    # Make a copy of the array to avoid side effects.
    arr_copy = arr.copy()
    start_time = time.perf_counter()
    sort_func(arr_copy)
    return time.perf_counter() - start_time

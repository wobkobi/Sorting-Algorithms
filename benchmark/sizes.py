"""
sizes.py

This module provides functions related to generating array sizes for benchmarking
and determining the number of worker processes to use based on system resources
and time of day.

Functions:
    generate_sizes()
    get_num_workers()
"""

import os
import datetime


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    Combines a geometrically-spaced set of small sizes with exponentially growing large sizes.

    Returns:
        list: Sorted list of unique array sizes.
    """
    n_small = 15
    # Generate small sizes using a geometric progression.
    small_sizes = [
        int(round(5 * ((200 / 3) ** (i / (n_small - 1))))) for i in range(n_small)
    ]
    large_sizes = []
    size = 100
    # Generate large sizes by doubling until reaching 1e12.
    while size < 1e12:
        large_sizes.append(int(size))
        size *= 2
    large_sizes.append(int(1e12))
    # Combine and sort the unique sizes.
    return sorted(set(small_sizes + large_sizes))


def get_num_workers():
    """
    Determine the number of worker processes for benchmarking.

    The function adjusts the number of workers based on:
      - Total CPU cores.
      - Time of day (more cores are used during night hours).
      - An optional "SLOW_MODE" environment variable to reduce worker count.

    Returns:
        int: Number of worker processes (at least 1).
    """
    total = os.cpu_count() or 1
    now = datetime.datetime.now().time()
    # Use 75% of cores at night, otherwise 50%.
    if datetime.time(23, 30) <= now or now <= datetime.time(9, 30):
        workers = max(int(total * 0.75), 1)
    else:
        workers = max(int(total * 0.5), 1)
    # If slow mode is enabled, reduce the count by half.
    if os.environ.get("SLOW_MODE", "").lower() == "true":
        workers = max(int(workers * 0.5), 1)
    return workers

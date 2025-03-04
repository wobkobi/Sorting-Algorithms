"""
sizes.py

Provides functions for generating benchmark array sizes and determining the number of worker processes.

Functions:
  - generate_sizes(): Returns a sorted list of unique array sizes.
  - get_num_workers(): Determines the worker count based on CPU cores, time of day, and SLOW_MODE.
"""

import os
import datetime


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    Combines a geometrically spaced set of small sizes with exponentially growing large sizes.

    Returns:
      list: Sorted list of unique array sizes.
    """
    n_small = 15
    # Geometrically spaced small sizes.
    small_sizes = [
        int(round(5 * ((200 / 3) ** (i / (n_small - 1))))) for i in range(n_small)
    ]
    large_sizes = []
    size = 100
    # Exponentially growing large sizes.
    while size < 1e12:
        large_sizes.append(int(size))
        size *= 2
    large_sizes.append(int(1e12))
    return sorted(set(small_sizes + large_sizes))


def get_num_workers():
    """
    Determine the number of worker processes for benchmarking.

    During night time (from 11:30 PM to 9:30 AM), the function uses all available cores
    except for 2 reserved for the OS. During other times, it uses 50% of the total cores.
    If the environment variable "SLOW_MODE" is set, the worker count is further halved.

    Returns:
      int: Number of worker processes (at least 1).
    """
    total = os.cpu_count() or 1
    now = datetime.datetime.now().time()

    # Night time: between 23:30 and 09:30.
    if datetime.time(23, 30) <= now or now <= datetime.time(9, 30):
        # Use all cores except for 2 reserved for the OS.
        workers = total - 2 if total > 2 else 1
    else:
        # Daytime: use 50% of the total cores.
        workers = max(int(total * 0.5), 1)
    # Adjust for slow mode.
    if os.environ.get("SLOW_MODE", "").lower() == "true":
        workers = max(int(workers * 0.5), 1)
    return workers

"""
sizes.py

Provides functions related to generating benchmark array sizes and determining the number of worker processes.
Includes:
  - generate_sizes(): Returns a sorted list of unique array sizes.
  - get_num_workers(): Calculates the worker count based on system resources and environment flags.
"""

import math
import os
import datetime
from .config import debug


def generic_round(x, base=25, tol=3):
    """
    Round number x to the nearest multiple of 'base' if within tolerance.

    Parameters:
      x (number): The number to round.
      base (number): The rounding base (default 25).
      tol (number): Tolerance for rounding (default 3).

    Returns:
      number: Rounded value or original x.
    """
    candidate = round(x / base) * base
    return candidate if abs(x - candidate) <= tol else x


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    Returns:
      list: Sorted list of array sizes.
    """
    n_small = 15
    small_sizes = [
        int(round(5 * ((200 / 3) ** (i / (n_small - 1))))) for i in range(n_small)
    ]
    small_sizes = [generic_round(x) for x in small_sizes]
    max_small = max(small_sizes)
    large_sizes = []
    factors = [2.5, 5, 7.5, 10]
    start_exp = math.ceil(math.log10(max_small))
    e = start_exp
    while True:
        base = 10 ** (e - 1)
        for f in factors:
            size_val = f * base
            if size_val > max_small:
                if size_val > 1e12:
                    break
                large_sizes.append(int(size_val))
        if factors[-1] * base > 1e12:
            break
        e += 1
    sizes = sorted(set(small_sizes + large_sizes))
    debug(f"Generated array sizes: {sizes[:10]}{'...' if len(sizes) > 10 else ''}")
    return sizes


def get_num_workers():
    """
    Determine the number of worker processes based on CPU cores, time of day, and mode flags.

    Returns:
      int: Number of worker processes (minimum 1).
    """
    total = os.cpu_count() or 1
    if (
        os.environ.get("GITHUB_ACTIONS", "false").lower() == "true"
        and os.environ.get("USE_ALL_CPUS", "false").lower() == "true"
    ):
        workers = total
    else:
        now = datetime.datetime.now().time()
        if datetime.time(23, 30) <= now or now <= datetime.time(9, 30):
            workers = total - 2 if total > 2 else 1
        else:
            workers = max(int(total * 0.5), 1)
        if os.environ.get("SLOW_MODE", "").lower() == "true":
            workers = max(int(workers * 0.5), 1)
        elif os.environ.get("FAST_MODE", "").lower() == "true":
            workers = max(total - 2, 1)
    debug(f"Calculated number of workers: {workers} (Total cores: {total})")
    return workers

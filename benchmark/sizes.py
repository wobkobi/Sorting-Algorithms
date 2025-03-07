"""
sizes.py

This module provides functions related to generating benchmark array sizes and
determining the number of worker processes to use for the benchmark.

Functions:
  - generate_sizes(): Produces a sorted list of unique array sizes.
  - get_num_workers(): Determines the worker count based on CPU cores, current time, and SLOW_MODE setting.
"""

import math
import os
import datetime


def generic_round(x, base=25, tol=3):
    """
    Round a number x to the nearest multiple of 'base' if the difference is within a given tolerance.

    This helper function checks if x is close enough to a multiple of 'base' (within tol)
    and returns the rounded value if so; otherwise, it returns x unchanged.

    Parameters:
      x (number): The number to potentially round.
      base (number): The multiple to round to (default is 25).
      tol (number): The maximum allowed difference for rounding (default is 3).

    Returns:
      number: The rounded value if within tolerance, or the original x.
    """
    candidate = round(x / base) * base
    if abs(x - candidate) <= tol:
        return candidate
    return x


def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.

    The function first generates a set of small sizes using a geometric progression.
    These sizes are then adjusted using a generic rounding function to round values
    to the nearest multiple of 25 (if within a specified tolerance). This ensures that
    values like 22, 74, or 247 are rounded to 25, 75, and 250 respectively.

    For sizes larger than the maximum small size, the function generates "nice" large sizes.
    These are computed using a set of factors [2.5, 5, 7.5, 10] applied to increasing
    powers of 10, ensuring that the large sizes are round numbers (e.g., 500, 750, 1000, 2500, etc.).

    The final list of sizes is the union of the adjusted small sizes and the generated large sizes,
    sorted in ascending order.

    Returns:
      list: A sorted list of unique array sizes.
    """
    n_small = 15

    # Generate small sizes using a geometric progression.
    # The formula 5 * ((200/3) ** (i/(n_small-1))) produces a range of sizes.
    small_sizes = [
        int(round(5 * ((200 / 3) ** (i / (n_small - 1))))) for i in range(n_small)
    ]
    # Apply generic rounding to each small size to "snap" values near multiples of 25.
    small_sizes = [generic_round(x) for x in small_sizes]
    max_small = max(small_sizes)

    large_sizes = []
    # Define factors that yield "nice" round numbers for large sizes.
    # Multiplying these factors by a power-of-10 base will produce sizes like 500, 750, 1000, etc.
    factors = [2.5, 5, 7.5, 10]

    # Determine the starting exponent for large sizes.
    # We want the smallest base (10^(e-1)) such that 1 * 10^(e-1) is greater than max_small.
    start_exp = math.ceil(math.log10(max_small))

    e = start_exp
    while True:
        base = 10 ** (e - 1)
        for f in factors:
            size_val = f * base
            # Only include the value if it exceeds the maximum of the small sizes.
            if size_val > max_small:
                # Stop adding if the size exceeds the upper bound of 1e12.
                if size_val > 1e12:
                    break
                large_sizes.append(int(size_val))
        # Exit the loop if the largest value in the current group exceeds 1e12.
        if factors[-1] * base > 1e12:
            break
        e += 1

    # Return the sorted union of small and large sizes.
    return sorted(set(small_sizes + large_sizes))


def get_num_workers():
    """
    Determine the number of worker processes for the benchmark.

    Priority:
      1. If running in GitHub Actions (GITHUB_ACTIONS == "true") and USE_ALL_CPUS is "true",
         use all available CPU cores (i.e. do not leave any cores free).
      2. Otherwise, determine the worker count based on:
         - Time of day:
             * During night time (11:30 PM to 9:30 AM), reserve 2 cores for the OS.
             * During daytime, use 50% of the total cores.
      3. Further adjust based on SLOW_MODE or FAST_MODE:
         - If SLOW_MODE is enabled, halve the worker count.
         - Else if FAST_MODE is enabled, use all cores minus 2.

    Returns:
      int: The number of worker processes (minimum of 1).
    """
    total = os.cpu_count() or 1

    # If running in GitHub Actions and USE_ALL_CPUS is set, return all cores.
    if (
        os.environ.get("GITHUB_ACTIONS", "false").lower() == "true"
        and os.environ.get("USE_ALL_CPUS", "false").lower() == "true"
    ):
        return total

    now = datetime.datetime.now().time()
    # Determine if it's night time (between 11:30 PM and 9:30 AM)
    if datetime.time(23, 30) <= now or now <= datetime.time(9, 30):
        workers = total - 2 if total > 2 else 1
    else:
        workers = max(int(total * 0.5), 1)

    if os.environ.get("SLOW_MODE", "").lower() == "true":
        workers = max(int(workers * 0.5), 1)
    elif os.environ.get("FAST_MODE", "").lower() == "true":
        workers = max(total - 2, 1)

    return workers

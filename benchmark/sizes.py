import os
import datetime

def generate_sizes():
    """
    Generate a sorted list of unique array sizes for benchmarking.
    """
    n_small = 15
    small_sizes = [
        int(round(5 * ((200 / 3) ** (i / (n_small - 1))))) for i in range(n_small)
    ]
    large_sizes = []
    size = 100
    while size < 1e12:
        large_sizes.append(int(size))
        size *= 2
    large_sizes.append(int(1e12))
    return sorted(set(small_sizes + large_sizes))

def get_num_workers():
    """
    Determine the number of worker processes to use.
    Adjusts the count based on the time of day and an optional SLOW_MODE environment variable.
    """
    total = os.cpu_count() or 1
    now = datetime.datetime.now().time()
    if datetime.time(23, 30) <= now or now <= datetime.time(9, 30):
        workers = max(int(total * 0.75), 1)
    else:
        workers = max(int(total * 0.5), 1)
    if os.environ.get("SLOW_MODE", "").lower() == "true":
        workers = max(int(workers * 0.5), 1)
    return workers

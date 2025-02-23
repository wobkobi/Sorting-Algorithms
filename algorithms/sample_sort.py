import math
from heapq import merge


def sample_sort(arr: list) -> list:
    """
    Sample Sort implementation.

    Time Complexity: Expected O(n log n)
    Space Complexity: O(n)

    Divides the array using a set of sample elements to determine splitters, then sorts subarrays—well-suited for parallel sorting.
    """
    if not arr:
        return arr
    n = len(arr)
    # Choose number of partitions (e.g. √n)
    k = int(math.sqrt(n)) or 1
    # Use a preliminary sort to choose pivots.
    arr_sorted = sorted(arr)
    step = n // k
    pivots = [arr_sorted[i * step] for i in range(1, k)]
    buckets = [[] for _ in range(k)]
    for x in arr:
        placed = False
        for pivot in pivots:
            if x < pivot:
                buckets[pivots.index(pivot)].append(x)
                placed = True
                break
        if not placed:
            buckets[-1].append(x)
    sorted_arr = []
    for bucket in buckets:
        sorted_arr = list(merge(sorted_arr, sorted(bucket)))
    return sorted_arr

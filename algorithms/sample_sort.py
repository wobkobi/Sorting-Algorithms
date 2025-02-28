# sample_sort.py
from heapq import merge
import math


def sample_sort(arr):
    """
    Sample Sort – uses a preliminary sort to choose splitters,
    partitions the array into buckets, sorts each, then merges.

    Time Complexity: Expected O(n log n)
    Space Complexity: O(n)
    """
    if not arr:
        return []
    n = len(arr)
    k = max(int(math.sqrt(n)), 1)
    arr_sorted = sorted(arr)
    step = n // k
    pivots = [arr_sorted[i * step] for i in range(1, k)]
    buckets = [[] for _ in range(k)]
    for x in arr:
        placed = False
        for idx, pivot in enumerate(pivots):
            if x < pivot:
                buckets[idx].append(x)
                placed = True
                break
        if not placed:
            buckets[-1].append(x)
    sorted_arr = []
    for bucket in buckets:
        sorted_arr = list(merge(sorted_arr, sorted(bucket)))
    return sorted_arr

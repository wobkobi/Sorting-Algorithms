# block_sort.py
from heapq import merge
import math


def block_sort(arr):
    """
    Block Sort – divides the array into blocks (of size ≈√n), sorts each block,
    then merges them.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if not arr:
        return []
    n = len(arr)
    block_size = max(int(math.sqrt(n)), 1)
    blocks = [sorted(arr[i : i + block_size]) for i in range(0, n, block_size)]
    sorted_arr = []
    for block in blocks:
        sorted_arr = list(merge(sorted_arr, block))
    return sorted_arr

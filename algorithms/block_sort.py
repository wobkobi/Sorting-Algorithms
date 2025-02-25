import math
from heapq import merge


def block_sort(arr: list) -> list:
    """
    Block Sort implementation.

    Time Complexity: O(n log n)
    Space Complexity: O(n)

    Divides the array into blocks, sorts each block, and then merges them. Suitable for large datasets.
    """
    if not arr:
        return arr

    n = len(arr)
    if n <= 1:
        return arr
    block_size = int(math.sqrt(n)) or 1
    # Sort each block.
    blocks = [sorted(arr[i : i + block_size]) for i in range(0, n, block_size)]
    # Merge all blocks.
    sorted_arr = []
    for block in blocks:
        sorted_arr = list(merge(sorted_arr, block))
    return sorted_arr

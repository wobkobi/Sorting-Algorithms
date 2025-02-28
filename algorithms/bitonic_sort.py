# bitonic_sort_parallel.py
import math
import concurrent.futures


def bitonic_merge(arr, ascending):
    n = len(arr)
    if n <= 1:
        return arr
    mid = n // 2
    for i in range(mid):
        if (arr[i] > arr[i + mid]) == ascending:
            arr[i], arr[i + mid] = arr[i + mid], arr[i]
    left = bitonic_merge(arr[:mid], ascending)
    right = bitonic_merge(arr[mid:], ascending)
    return left + right


def _bitonic_sort_recursive(arr, ascending, threshold, executor=None):
    n = len(arr)
    if n <= 1:
        return arr
    mid = n // 2
    if executor is not None and n >= threshold:
        future_left = executor.submit(
            _bitonic_sort_recursive, arr[:mid], True, threshold, None
        )
        future_right = executor.submit(
            _bitonic_sort_recursive, arr[mid:], False, threshold, None
        )
        left = future_left.result()
        right = future_right.result()
    else:
        left = _bitonic_sort_recursive(arr[:mid], True, threshold, None)
        right = _bitonic_sort_recursive(arr[mid:], False, threshold, None)
    combined = left + right
    return bitonic_merge(combined, ascending)


def bitonic_sort_parallel(arr, ascending=True, threshold=1024):
    """
    Parallel Bitonic Sort – pads array to a power of two and sorts using parallel recursion.

    Time Complexity: O(n log² n) sequentially; potential parallel speedup.
    Space Complexity: O(n)
    """
    if not arr:
        return []
    n = len(arr)
    next_power = 2 ** math.ceil(math.log2(n))
    pad_value = float("inf") if ascending else float("-inf")
    padded = arr + [pad_value] * (next_power - n)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        sorted_padded = _bitonic_sort_recursive(padded, ascending, threshold, executor)
    return sorted_padded[:n]

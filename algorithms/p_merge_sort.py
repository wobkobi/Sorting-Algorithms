import concurrent.futures
from heapq import merge


def _parallel_merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = _parallel_merge_sort(arr[:mid])
    right = _parallel_merge_sort(arr[mid:])
    return list(merge(left, right))


def p_merge_sort(arr: list) -> list:
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    with concurrent.futures.ProcessPoolExecutor() as executor:
        left_future = executor.submit(_parallel_merge_sort, arr[:mid])
        right_future = executor.submit(_parallel_merge_sort, arr[mid:])
        left = left_future.result()
        right = right_future.result()
    return list(merge(left, right))

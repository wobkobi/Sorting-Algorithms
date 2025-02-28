# bucket_sort.py
from .insertion_sort import insertion_sort


def bucket_sort(arr):
    """
    Bucket Sort – distributes elements into buckets, sorts each bucket
    (using insertion sort), then concatenates.

    Time Complexity: Average O(n + k), worst-case O(n²)
    Space Complexity: O(n + k)
    """
    if not arr:
        return []
    min_val = min(arr)
    max_val = max(arr)
    bucket_count = len(arr)
    buckets = [[] for _ in range(bucket_count)]
    for num in arr:
        index = (
            (num - min_val) * (bucket_count - 1) // (max_val - min_val)
            if max_val != min_val
            else 0
        )
        buckets[index].append(num)
    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(insertion_sort(bucket))
    return sorted_arr

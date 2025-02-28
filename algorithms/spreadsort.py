# spreadsort.py
from .insertion_sort import insertion_sort


def spreadsort(arr):
    """
    Spreadsort.

    Time Complexity: Expected O(n)
    Space Complexity: O(n)

    A bucket-based sorting algorithm that first "spreads" the elements into buckets
    based on their normalized value, then sorts each bucket using insertion sort.
    """
    if not arr:
        return []

    n = len(arr)
    # Determine the minimum and maximum values.
    minimum = arr[0]
    maximum = arr[0]
    for x in arr:
        if x < minimum:
            minimum = x
        if x > maximum:
            maximum = x

    # If all elements are equal, return a copy.
    if minimum == maximum:
        return arr[:]

    # Create buckets. We'll use n buckets.
    buckets = [[] for _ in range(n)]
    range_val = maximum - minimum

    # Distribute elements into buckets.
    for x in arr:
        # Normalize value to a bucket index in [0, n-1]
        index = int(((x - minimum) / range_val) * (n - 1))
        buckets[index].append(x)

    sorted_arr = []
    for bucket in buckets:
        if bucket:
            sorted_bucket = insertion_sort(bucket)
            sorted_arr.extend(sorted_bucket)

    # Copy the sorted result back into the original array.
    for i in range(n):
        arr[i] = sorted_arr[i]
    return arr

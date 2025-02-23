def insertion_sort(arr: list, left: int, right: int) -> None:
    """Sorts the portion of the array from index left to right (inclusive)
    using insertion sort."""
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge(arr: list, left: int, mid: int, right: int) -> None:
    """Merges two sorted subarrays:
    arr[left:mid+1] and arr[mid+1:right+1] into a single sorted subarray."""
    # Create temporary arrays for left and right runs.
    left_run = arr[left : mid + 1]
    right_run = arr[mid + 1 : right + 1]

    i = j = 0
    k = left

    # Merge the temporary arrays back into arr[left:right+1].
    while i < len(left_run) and j < len(right_run):
        if left_run[i] <= right_run[j]:
            arr[k] = left_run[i]
            i += 1
        else:
            arr[k] = right_run[j]
            j += 1
        k += 1

    # Copy any remaining elements of left_run, if any.
    while i < len(left_run):
        arr[k] = left_run[i]
        i += 1
        k += 1

    # Copy any remaining elements of right_run, if any.
    while j < len(right_run):
        arr[k] = right_run[j]
        j += 1
        k += 1


def tim_sort(arr: list) -> list:
    """
    Tim Sort implementation.

    Time Complexity: Best-case O(n), Worst-case O(n log n)
    Space Complexity: O(n)

    A hybrid stable sort combining merge sort and insertion sort, highly optimized for real-world data and widely used in programming languages.
    """
    n = len(arr)
    if n < 2:
        return arr

    # Define a minimum run size; 32 is a common choice.
    min_run = 32

    # Sort individual subarrays of size min_run using insertion sort.
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort(arr, start, end)

    # Start merging from size min_run (or 32). Double the size each iteration.
    size = min_run
    while size < n:
        # Pick starting point of left run.
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min((left + 2 * size - 1), n - 1)
            if mid < right:
                merge(arr, left, mid, right)
        size *= 2

    return arr

# tim_sort.py
def insertion_sort_range(arr, left, right):
    for i in range(left + 1, right + 1):
        key = arr[i]
        j = i - 1
        while j >= left and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key


def merge_range(arr, left, mid, right):
    left_run = arr[left : mid + 1]
    right_run = arr[mid + 1 : right + 1]
    i = j = 0
    k = left
    while i < len(left_run) and j < len(right_run):
        if left_run[i] <= right_run[j]:
            arr[k] = left_run[i]
            i += 1
        else:
            arr[k] = right_run[j]
            j += 1
        k += 1
    while i < len(left_run):
        arr[k] = left_run[i]
        i += 1
        k += 1
    while j < len(right_run):
        arr[k] = right_run[j]
        j += 1
        k += 1


def tim_sort(arr):
    """
    Tim Sort – hybrid sort combining insertion sort and merge sort (as used in Python's sorted()).

    Time Complexity: Best-case O(n), worst-case O(n log n)
    Space Complexity: O(n)
    """
    if not arr:
        return []
    a = arr[:]
    n = len(a)
    min_run = 32
    for start in range(0, n, min_run):
        end = min(start + min_run - 1, n - 1)
        insertion_sort_range(a, start, end)
    size = min_run
    while size < n:
        for left in range(0, n, 2 * size):
            mid = min(n - 1, left + size - 1)
            right = min(left + 2 * size - 1, n - 1)
            if mid < right:
                merge_range(a, left, mid, right)
        size *= 2
    return a

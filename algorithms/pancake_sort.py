# pancake_sort.py
def flip(arr, i):
    return arr[: i + 1][::-1] + arr[i + 1 :]


def find_max(arr, n):
    max_index = 0
    for i in range(1, n):
        if arr[i] > arr[max_index]:
            max_index = i
    return max_index


def pancake_sort(arr):
    """
    Pancake Sort – repeatedly flips the array to move the maximum element into place.

    Time Complexity: O(n²)
    Space Complexity: O(1)
    """
    if not arr:
        return []
    a = arr[:]
    n = len(a)
    for curr_size in range(n, 1, -1):
        max_index = find_max(a, curr_size)
        if max_index != curr_size - 1:
            a = flip(a, max_index)
            a = flip(a, curr_size - 1)
    return a

def pancake_sort(arr: list) -> list:
    """
    Pancake Sort implementation.

    Time Complexity: O(n²)
    Space Complexity: O(1)

    Sorts the array by repeatedly flipping portions of the list, analogous to sorting a stack of pancakes.
    """
    n = len(arr)
    for curr_size in range(n, 1, -1):
        max_index = find_max(arr, curr_size)
        if max_index != curr_size - 1:
            arr = flip(arr, max_index)
            arr = flip(arr, curr_size - 1)
    return arr


def flip(arr: list, i: int) -> list:
    return arr[: i + 1][::-1] + arr[i + 1 :]


def find_max(arr: list, n: int) -> int:
    max_index = 0
    for i in range(1, n):
        if arr[i] > arr[max_index]:
            max_index = i
    return max_index

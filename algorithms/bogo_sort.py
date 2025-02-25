import random


def is_sorted(arr: list) -> bool:
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True


def bogo_sort(arr: list) -> list:
    """
    Bogo Sort implementation.

    Time Complexity: Average-case O((n+1)!) (practically unbounded)
    Space Complexity: O(1)

    Randomly shuffles the array until sorted. Only useful for very small arrays or educational purposes.
    """
    if not arr:
        return arr

    while not is_sorted(arr):
        random.shuffle(arr)
    return arr

# bogo_sort.py
import random


def is_sorted(arr):
    return all(arr[i] <= arr[i + 1] for i in range(len(arr) - 1))


def bogo_sort(arr):
    """
    Bogo Sort – randomly shuffles until sorted. (Educational only.)

    Time Complexity: Average-case O((n+1)!)
    Space Complexity: O(1)
    """
    if not arr:
        return []
    a = arr[:]
    while not is_sorted(a):
        random.shuffle(a)
    return a

# tournament_sort.py
import math


def tournament_sort(arr):
    """
    Tournament Sort – builds a tournament tree to repeatedly extract the minimum.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if not arr:
        return []
    n = len(arr)
    size = 2 ** math.ceil(math.log2(n))
    tree = [None] * (2 * size)
    for i in range(size):
        tree[size + i] = arr[i] if i < n else float("inf")
    for i in range(size - 1, 0, -1):
        tree[i] = min(tree[2 * i], tree[2 * i + 1])
    sorted_arr = []
    for _ in range(n):
        min_val = tree[1]
        sorted_arr.append(min_val)
        index = next(i for i in range(size, 2 * size) if tree[i] == min_val)
        tree[index] = float("inf")
        i = index // 2
        while i >= 1:
            tree[i] = min(tree[2 * i], tree[2 * i + 1])
            i //= 2
    return sorted_arr

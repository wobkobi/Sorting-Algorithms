import math


def tournament_sort(arr: list) -> list:
    if not arr:
        return arr
    n = len(arr)
    size = 2 ** math.ceil(math.log2(n))
    tree = [None] * (2 * size)
    # Place elements at leaves; pad with infinity.
    for i in range(size):
        tree[size + i] = arr[i] if i < n else float("inf")
    # Build the tournament tree.
    for i in range(size - 1, 0, -1):
        tree[i] = min(tree[2 * i], tree[2 * i + 1])
    sorted_arr = []
    for _ in range(n):
        min_val = tree[1]
        sorted_arr.append(min_val)
        # Find and update the leaf containing min_val.
        index = -1
        for i in range(size, 2 * size):
            if tree[i] == min_val:
                index = i
                break
        tree[index] = float("inf")
        i = index // 2
        while i >= 1:
            tree[i] = min(tree[2 * i], tree[2 * i + 1])
            i //= 2
    return sorted_arr

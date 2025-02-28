# sorting_network.py
import math


def sorting_network(arr):
    """
    Sorting Network (via Bitonic Sort) – pads the array to a power of two
    and sorts using a bitonic merge network.

    Time Complexity: O(n log² n)
    Space Complexity: O(n)
    """
    if not arr:
        return []
    n = len(arr)
    power = 2 ** int(math.ceil(math.log2(n)))
    padded = arr[:] + [float("inf")] * (power - n)

    def bitonic_merge(a, lo, n, direction):
        if n > 1:
            k = n // 2
            for i in range(lo, lo + k):
                if (direction == 1 and a[i] > a[i + k]) or (
                    direction == 0 and a[i] < a[i + k]
                ):
                    a[i], a[i + k] = a[i + k], a[i]
            bitonic_merge(a, lo, k, direction)
            bitonic_merge(a, lo + k, k, direction)

    def bitonic_sort_rec(a, lo, n, direction):
        if n > 1:
            k = n // 2
            bitonic_sort_rec(a, lo, k, 1)
            bitonic_sort_rec(a, lo + k, k, 0)
            bitonic_merge(a, lo, n, direction)

    bitonic_sort_rec(padded, 0, power, 1)
    return [x for x in padded if x != float("inf")]

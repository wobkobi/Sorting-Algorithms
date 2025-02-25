def sorting_network(arr: list) -> list:
    """
    Sorting Network (via Bitonic Sort).

    Time Complexity: O(n log² n)
    Space Complexity: O(n)

    Implements a sorting network using a bitonic merge approach. Note that this
    implementation pads the array to the next power of two.
    """
    import math

    if not arr:
        return arr

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
    sorted_arr = [x for x in padded if x != float("inf")]
    arr[:] = sorted_arr
    return arr

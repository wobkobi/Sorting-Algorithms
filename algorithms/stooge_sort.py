# stooge_sort.py
def stooge_sort(arr):
    """
    Stooge Sort – a recursive, highly inefficient sorting algorithm.

    Time Complexity: Approximately O(n^(2.7))
    Space Complexity: O(1)
    """
    a = arr[:]

    def stooge_sort_recursive(a, i, j):
        if a[j] < a[i]:
            a[i], a[j] = a[j], a[i]
        if j - i + 1 > 2:
            t = (j - i + 1) // 3
            stooge_sort_recursive(a, i, j - t)
            stooge_sort_recursive(a, i + t, j)
            stooge_sort_recursive(a, i, j - t)

    stooge_sort_recursive(a, 0, len(a) - 1)
    return a

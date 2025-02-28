# exchange_sort.py
def exchange_sort(arr):
    """
    Exchange Sort – repeatedly swaps out-of-order elements.

    Time Complexity: O(n²)
    Space Complexity: O(1)
    """
    if not arr:
        return []
    a = arr[:]
    n = len(a)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if a[i] > a[j]:
                a[i], a[j] = a[j], a[i]
    return a

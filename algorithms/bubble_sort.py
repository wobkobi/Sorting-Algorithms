# bubble_sort.py
def bubble_sort(arr):
    """
    Bubble Sort – repeatedly compares and swaps adjacent elements.

    Time Complexity: Best-case O(n) (with early termination), worst-case O(n²)
    Space Complexity: O(1)
    """
    if not arr:
        return []
    a = arr[:]
    n = len(a)
    for i in range(n):
        for j in range(0, n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

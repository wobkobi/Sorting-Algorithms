# selection_sort.py
def selection_sort(arr):
    """
    Selection Sort – repeatedly selects the minimum element and swaps.

    Time Complexity: O(n²)
    Space Complexity: O(1)
    """
    if not arr:
        return []
    a = arr[:]
    n = len(a)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if a[j] < a[min_idx]:
                min_idx = j
        a[i], a[min_idx] = a[min_idx], a[i]
    return a

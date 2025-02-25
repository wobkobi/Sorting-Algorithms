def bubble_sort(arr: list) -> list:
    """
    Bubble Sort implementation.

    Time Complexity: Best-case O(n) (optimized), Worst-case O(n²)
    Space Complexity: O(1)

    Repeatedly compares and swaps adjacent elements. Simple but inefficient on large lists.
    """
    if not arr:
        return arr

    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def exchange_sort(arr: list) -> list:
    """
    Exchange Sort implementation.

    Time Complexity: O(n^2)
    Space Complexity: O(1)

    This is a stub implementation.
    """
    if not arr:
        return arr

    n = len(arr)
    for i in range(n - 1):
        for j in range(i + 1, n):
            if arr[i] > arr[j]:
                arr[i], arr[j] = arr[j], arr[i]
    return arr

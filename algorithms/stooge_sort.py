def stooge_sort(arr: list) -> list:
    return stooge_sort_recursive(arr, 0, len(arr) - 1)


def stooge_sort_recursive(arr: list, i: int, j: int) -> list:
    """
    Stooge Sort implementation.

    Time Complexity: Approximately O(n^(2.7)) (highly inefficient)
    Space Complexity: O(1)

    A recursive sorting algorithm primarily of academic interest due to its very poor performance.
    """
    if not arr:
        return arr

    if arr[j] < arr[i]:
        arr[i], arr[j] = arr[j], arr[i]
    if j - i + 1 > 2:
        t = (j - i + 1) // 3
        arr = stooge_sort_recursive(arr, i, j - t)
        arr = stooge_sort_recursive(arr, i + t, j)
        arr = stooge_sort_recursive(arr, i, j - t)
    return arr

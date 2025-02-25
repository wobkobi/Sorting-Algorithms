def slowsort(arr: list, i=0, j=None) -> list:
    """
    Slowsort.

    Time Complexity: O(n^(log₂ n)) (extremely inefficient)
    Space Complexity: O(1) (in-place)

    A deliberately inefficient recursive sorting algorithm.
    """
    if not arr:
        return arr

    if j is None:
        j = len(arr) - 1
    if i >= j:
        return
    m = (i + j) // 2
    slowsort(arr, i, m)
    slowsort(arr, m + 1, j)
    if arr[j] < arr[m]:
        arr[j], arr[m] = arr[m], arr[j]
    slowsort(arr, i, j - 1)
    return arr

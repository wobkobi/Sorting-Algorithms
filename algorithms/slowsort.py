# slowsort.py
def slowsort(arr, i=0, j=None):
    """
    Slowsort – a deliberately inefficient recursive sorting algorithm.

    Time Complexity: Approximately O(n^(log₂ n)) (extremely inefficient)
    Space Complexity: O(1) (in-place)
    """
    if not arr:
        return []
    if j is None:
        j = len(arr) - 1
    if i >= j:
        return arr
    m = (i + j) // 2
    slowsort(arr, i, m)
    slowsort(arr, m + 1, j)
    if arr[j] < arr[m]:
        arr[j], arr[m] = arr[m], arr[j]
    slowsort(arr, i, j - 1)
    return arr

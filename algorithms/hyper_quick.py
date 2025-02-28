# hyper_quick.py
def hyper_quick(arr):
    """
    Hyper Quick – a quicksort variant using the median-of-three pivot.

    Time Complexity: Expected O(n log n), worst-case O(n²)
    Space Complexity: O(log n)
    """
    if not arr:
        return []
    if len(arr) <= 1:
        return arr[:]
    first, mid, last = arr[0], arr[len(arr) // 2], arr[-1]
    pivot = sorted([first, mid, last])[1]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return hyper_quick(left) + middle + hyper_quick(right)

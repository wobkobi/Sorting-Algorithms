def hyper_quick(arr: list) -> list:
    """
    Hyper Quick implementation.

    Time Complexity: Expected O(n log n), Worst-case O(n²)
    Space Complexity: O(log n) average due to recursion

    A variant of quick sort with advanced pivot selection and partitioning optimizations.
    """
    if not arr:
        return arr

    if len(arr) <= 1:
        return arr
    first, mid, last = arr[0], arr[len(arr) // 2], arr[-1]
    pivot = sorted([first, mid, last])[1]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return hyper_quick(left) + middle + hyper_quick(right)

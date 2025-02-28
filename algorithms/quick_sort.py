# quick_sort.py
def quick_sort(arr):
    """
    Quick Sort – classic recursive implementation with pivot selection.

    Time Complexity: Average O(n log n), worst-case O(n²)
    Space Complexity: O(log n) on average (recursion)
    """
    if not arr:
        return []
    if len(arr) <= 1:
        return arr[:]
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

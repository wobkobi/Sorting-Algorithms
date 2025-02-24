def quick_sort(arr: list) -> list:
    """
    Quick Sort implementation.

    Time Complexity: Average-case O(n log n), Worst-case O(n²)
    Space Complexity: O(log n) average (due to recursion)

    Selects a pivot to partition the array and recursively sorts the subarrays. Widely used for its average performance.
    """
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

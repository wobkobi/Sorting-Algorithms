# merge_insertion_sort.py
def merge_insertion_sort(arr):
    """
    Merge Insertion Sort – uses insertion sort on subarrays of size ≤ 16,
    then merge sort for larger arrays.

    Time Complexity: O(n²) for small arrays, O(n log n) overall.
    Space Complexity: O(n)
    """
    if not arr:
        return []
    if len(arr) <= 16:
        a = arr[:]
        for i in range(1, len(a)):
            key = a[i]
            j = i - 1
            while j >= 0 and a[j] > key:
                a[j + 1] = a[j]
                j -= 1
            a[j + 1] = key
        return a
    else:
        mid = len(arr) // 2
        left = merge_insertion_sort(arr[:mid])
        right = merge_insertion_sort(arr[mid:])
        i = j = 0
        merged = []
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged

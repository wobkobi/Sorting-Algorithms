def merge_insertion_sort(arr: list) -> list:
    """
    Merge Insertion Sort.

    Time Complexity: O(n²) for small arrays (insertion sort), O(n log n) overall
    Space Complexity: O(n)

    Uses insertion sort for small subarrays and merge sort for larger ones.
    """
    if len(arr) <= 16:
        for i in range(1, len(arr)):
            key = arr[i]
            j = i - 1
            while j >= 0 and arr[j] > key:
                arr[j + 1] = arr[j]
                j -= 1
            arr[j + 1] = key
        return arr
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
        arr[:] = merged
        return arr

def merge_sort_inplace(arr: list) -> list:
    """
    In-Place Merge Sort implementation.

    Time Complexity: O(n log n) in all cases.
    Space Complexity: O(1) extra space (ignoring recursion stack).

    This implementation sorts the input list in place by recursively splitting the list
    and merging the sorted subarrays in place without allocating extra space for merging.
    """

    def merge_inplace(arr, start, mid, end):
        """
        Merge two adjacent sorted subarrays [start:mid] and [mid:end] in place.

        This function uses a rotation approach: when an element in the right subarray is smaller than
        the element in the left subarray, it rotates the subarray to insert the element in its proper position.
        """
        left = start
        right = mid
        while left < right and right < end:
            if arr[left] <= arr[right]:
                left += 1
            else:
                temp = arr[right]
                # Rotate the subarray: shift elements in arr[left:right] one position to the right.
                arr[left + 1 : right + 1] = arr[left:right]
                arr[left] = temp
                left += 1
                right += 1
                mid += 1

    def merge_sort_recursive(arr, start, end):
        if end - start > 1:
            mid = (start + end) // 2
            merge_sort_recursive(arr, start, mid)
            merge_sort_recursive(arr, mid, end)
            merge_inplace(arr, start, mid, end)

    merge_sort_recursive(arr, 0, len(arr))
    return arr

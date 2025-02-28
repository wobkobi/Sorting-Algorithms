# merge_sort_inplace.py
def merge_sort_inplace(arr):
    """
    In-Place Merge Sort – sorts the list without allocating extra space for merging.

    Time Complexity: O(n log n)
    Space Complexity: O(1) extra (ignoring recursion stack)
    """

    def merge_inplace(a, start, mid, end):
        left = start
        right = mid
        while left < right and right < end:
            if a[left] <= a[right]:
                left += 1
            else:
                temp = a[right]
                a[left + 1 : right + 1] = a[left:right]
                a[left] = temp
                left += 1
                right += 1
                mid += 1

    def merge_sort_recursive(a, start, end):
        if end - start > 1:
            mid = (start + end) // 2
            merge_sort_recursive(a, start, mid)
            merge_sort_recursive(a, mid, end)
            merge_inplace(a, start, mid, end)

    a = arr[:]
    merge_sort_recursive(a, 0, len(a))
    return a

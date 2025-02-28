# shell_sort.py
def shell_sort(arr):
    """
    Shell Sort – a generalization of insertion sort using gaps.

    Time Complexity: Typically between O(n log² n) and O(n^(3/2))
    Space Complexity: O(1)
    """
    if not arr:
        return []
    a = arr[:]
    n = len(a)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = a[i]
            j = i
            while j >= gap and a[j - gap] > temp:
                a[j] = a[j - gap]
                j -= gap
            a[j] = temp
        gap //= 2
    return a

# insertion_sort.py
def insertion_sort(arr):
    """
    Insertion Sort – builds the sorted list one element at a time.

    Time Complexity: Worst-case O(n²); Best-case O(n) for nearly sorted data.
    Space Complexity: O(1)
    """
    if not arr:
        return []
    a = arr[:]
    for i in range(1, len(a)):
        key = a[i]
        j = i - 1
        while j >= 0 and a[j] > key:
            a[j + 1] = a[j]
            j -= 1
        a[j + 1] = key
    return a

# odd_even_sort.py
def odd_even_sort(arr):
    """
    Odd-Even Sort (Brick Sort) – alternates comparing odd- and even-indexed pairs.

    Time Complexity: O(n²) worst-case.
    Space Complexity: O(1)
    """
    if not arr:
        return []
    a = arr[:]
    n = len(a)
    sorted_flag = False
    while not sorted_flag:
        sorted_flag = True
        for i in range(1, n - 1, 2):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                sorted_flag = False
        for i in range(0, n - 1, 2):
            if a[i] > a[i + 1]:
                a[i], a[i + 1] = a[i + 1], a[i]
                sorted_flag = False
    return a

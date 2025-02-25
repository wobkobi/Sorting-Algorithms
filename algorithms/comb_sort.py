def comb_sort(arr: list) -> list:
    """
    Comb Sort implementation.

    Time Complexity: Average-case better than bubble sort, but worst-case O(n²)
    Space Complexity: O(1)

    Improves on bubble sort by using a gap sequence to eliminate small values at the end of the list.
    """
    if not arr:
        return arr

    n = len(arr)
    gap = n
    shrink = 1.3
    sorted_flag = False
    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True
        i = 0
        while i + gap < n:
            if arr[i] > arr[i + gap]:
                arr[i], arr[i + gap] = arr[i + gap], arr[i]
                sorted_flag = False
            i += 1
    return arr

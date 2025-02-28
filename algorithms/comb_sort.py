# comb_sort.py
def comb_sort(arr):
    """
    Comb Sort – an improvement over bubble sort using a gap sequence.

    Time Complexity: Average-case better than bubble sort; worst-case O(n²)
    Space Complexity: O(1)
    """
    if not arr:
        return []
    a = arr[:]
    n = len(a)
    gap = n
    shrink = 1.3
    sorted_flag = False
    while not sorted_flag:
        gap = int(gap / shrink)
        if gap <= 1:
            gap = 1
            sorted_flag = True
        for i in range(n - gap):
            if a[i] > a[i + gap]:
                a[i], a[i + gap] = a[i + gap], a[i]
                sorted_flag = False
    return a

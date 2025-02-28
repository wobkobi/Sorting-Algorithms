# franceschinis_method.py
def franceschinis_method(arr):
    """
    Franceschini's Method – a three-way partitioning quicksort.

    Time Complexity: Average O(n log n)
    Space Complexity: O(log n)
    """

    def _three_way_quicksort(lst, low, high):
        if low >= high:
            return
        pivot = lst[low]
        lt, gt = low, high
        i = low
        while i <= gt:
            if lst[i] < pivot:
                lst[lt], lst[i] = lst[i], lst[lt]
                lt += 1
                i += 1
            elif lst[i] > pivot:
                lst[i], lst[gt] = lst[gt], lst[i]
                gt -= 1
            else:
                i += 1
        _three_way_quicksort(lst, low, lt - 1)
        _three_way_quicksort(lst, gt + 1, high)

    if not arr:
        return []
    a = arr[:]
    _three_way_quicksort(a, 0, len(a) - 1)
    return a

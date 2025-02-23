def franceschinis_method(arr: list) -> list:
    """
    Franceschini's Method.
    
    Time Complexity: O(n log n) average-case
    Space Complexity: O(log n) average due to recursion
    
    A custom 3-way partitioning quicksort implementation that recursively sorts
    the list without using any built-in sort.
    """
    def _three_way_quicksort(lst, low, high):
        if low >= high:
            return
        # Partition into three parts: < pivot, == pivot, > pivot.
        lt = low
        gt = high
        pivot = lst[low]
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
    
    _three_way_quicksort(arr, 0, len(arr) - 1)
    return arr

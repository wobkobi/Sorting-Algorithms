# library_sort.py
def library_sort(arr):
    """
    Library Sort – a gapped insertion sort inspired by library shelving.

    Time Complexity: Expected O(n log n)
    Space Complexity: O(n)
    """
    if not arr:
        return []
    n = len(arr)
    gap_factor = 2
    lib = [None] * (gap_factor * n)
    mid = len(lib) // 2
    lib[mid] = arr[0]
    for item in arr[1:]:
        low, high = 0, len(lib)
        while low < high:
            m = (low + high) // 2
            if lib[m] is None or lib[m] >= item:
                high = m
            else:
                low = m + 1
        idx = low
        while idx < len(lib) and lib[idx] is not None:
            idx += 1
        if idx == len(lib):
            new_lib = [None] * (len(lib) * 2)
            j = 0
            for x in lib:
                if x is not None:
                    new_lib[j * 2] = x
                    j += 1
            lib = new_lib
            idx = low
            while idx < len(lib) and lib[idx] is not None:
                idx += 1
        lib[idx] = item
    return [x for x in lib if x is not None]

def library_sort(arr: list) -> list:
    """
    Library Sort.

    Time Complexity: O(n log n) expected
    Space Complexity: O(n)

    Implements a gapped insertion sort that simulates the way library shelves
    leave gaps for future insertions.
    """
    if not arr:
        return arr
    n = len(arr)
    gap_factor = 2  # Determines the spacing; tweak as needed.
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
    sorted_arr = [x for x in lib if x is not None]
    arr[:] = sorted_arr
    return arr

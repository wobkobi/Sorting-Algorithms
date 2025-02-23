def p_merge_sort(arr: list) -> list:
    """
    Parallel Merge Sort.

    Time Complexity: O(n log n) (with parallelism)
    Space Complexity: O(n)

    Uses process-based parallelism for sorting large arrays.
    """
    if len(arr) <= 500:
        return sorted(arr)
    from concurrent.futures import ProcessPoolExecutor

    mid = len(arr) // 2
    with ProcessPoolExecutor() as executor:
        left_future = executor.submit(p_merge_sort, arr[:mid])
        right_future = executor.submit(p_merge_sort, arr[mid:])
        left = left_future.result()
        right = right_future.result()
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

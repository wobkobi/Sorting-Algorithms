import concurrent.futures


def bitonic_merge(arr: list, ascending: bool) -> list:
    """
    Bitonic Merge implementation.

    Time Complexity: O(n log² n)
    Space Complexity: O(n)

    Merges two bitonic sequences.
    """
    if not arr:
        return arr

    n = len(arr)
    if n <= 1:
        return arr
    mid = n // 2
    for i in range(mid):
        if (arr[i] > arr[i + mid]) == ascending:
            arr[i], arr[i + mid] = arr[i + mid], arr[i]
    left = bitonic_merge(arr[:mid], ascending)
    right = bitonic_merge(arr[mid:], ascending)
    return left + right


def _bitonic_sort_recursive(
    arr: list,
    ascending: bool,
    executor: concurrent.futures.ProcessPoolExecutor,
    threshold: int,
) -> list:
    """
    Recursive helper function for Bitonic Sort Parallel.
    """
    n = len(arr)
    if n <= 1:
        return arr

    mid = n // 2
    if n >= threshold:
        left_future = executor.submit(
            _bitonic_sort_recursive, arr[:mid], True, executor, threshold
        )
        right_future = executor.submit(
            _bitonic_sort_recursive, arr[mid:], False, executor, threshold
        )
        left = left_future.result()
        right = right_future.result()
    else:
        left = _bitonic_sort_recursive(arr[:mid], True, executor, threshold)
        right = _bitonic_sort_recursive(arr[mid:], False, executor, threshold)
    combined = left + right
    return bitonic_merge(combined, ascending)


def bitonic_sort_parallel(
    arr: list, ascending: bool = True, threshold: int = 1024
) -> list:
    """
    Bitonic Sort Parallel implementation.

    Time Complexity: O(n log² n) sequentially, O(log² n) with full parallelism
    Space Complexity: O(n)

    Constructs bitonic sequences and merges them. Highly effective on parallel architectures.
    """
    n = len(arr)
    if n == 0:
        return arr
    next_power = 1 << ((n - 1).bit_length())
    if next_power != n:
        pad_value = float("inf") if ascending else float("-inf")
        arr = arr + [pad_value] * (next_power - n)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        sorted_arr = _bitonic_sort_recursive(arr, ascending, executor, threshold)
    return sorted_arr[:n]

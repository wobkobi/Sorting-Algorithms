def msd_radix_sort(arr: list, digit=None) -> list:
    """
    MSD Radix Sort.

    Time Complexity: O(nk), where k is the number of digits
    Space Complexity: O(n)

    A non-in-place version that recursively sorts based on the most significant digit.
    """
    if len(arr) <= 1:
        return arr
    if digit is None:
        max_val = max(arr)
        digit = len(str(max_val))
    buckets = [[] for _ in range(10)]
    for num in arr:
        d = (num // (10 ** (digit - 1))) % 10
        buckets[d].append(num)
    result = []
    for bucket in buckets:
        if bucket:
            if digit - 1 > 0:
                bucket = msd_radix_sort(bucket, digit - 1)
            result.extend(bucket)
    return result

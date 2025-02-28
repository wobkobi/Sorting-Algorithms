# msd_radix_sort.py
def msd_radix_sort(arr, digit=None):
    """
    MSD Radix Sort (non-in-place) – recursively sorts by the most significant digit.

    Time Complexity: O(nk) where k is the number of digits.
    Space Complexity: O(n)
    """
    if not arr:
        return []
    if len(arr) <= 1:
        return arr[:]
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


# msd_radix_sort_inplace.py
def msd_radix_sort_inplace(arr, digit=None):
    """
    MSD Radix Sort In-Place – similar to the non-in-place version but writes directly into arr.

    Time Complexity: O(nk)
    Space Complexity: O(n)
    """
    if not arr:
        return []
    if len(arr) <= 1:
        return arr
    if digit is None:
        max_val = max(arr)
        digit = len(str(max_val))
    buckets = [[] for _ in range(10)]
    for num in arr:
        d = (num // (10 ** (digit - 1))) % 10
        buckets[d].append(num)
    index = 0
    for i in range(10):
        if buckets[i]:
            if digit - 1 > 0:
                buckets[i] = msd_radix_sort_inplace(buckets[i], digit - 1)
            for num in buckets[i]:
                arr[index] = num
                index += 1
    return arr

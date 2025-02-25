def msd_radix_sort_inplace(arr: list, digit=None) -> list:
    """
    MSD Radix Sort In-Place.

    Time Complexity: O(nk), where k is the number of digits
    Space Complexity: O(n)

    Recursively sorts the array by the most significant digit, then works in-place.
    """
    if not arr:
        return arr

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
                msd_radix_sort_inplace(buckets[i], digit - 1)
            for num in buckets[i]:
                arr[index] = num
                index += 1
    return arr

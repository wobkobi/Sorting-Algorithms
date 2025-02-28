# burst_sort.py
def burst_sort(arr):
    """
    Burst Sort – assigns numbers to fixed-width buckets and “bursts” large ones.

    Time Complexity: Expected O(n) average.
    Space Complexity: O(n)
    """
    if not arr:
        return []
    bucket_width = 100
    buckets = {}
    for x in arr:
        index = (
            (x // bucket_width) if x >= 0 else ((x - bucket_width + 1) // bucket_width)
        )
        buckets.setdefault(index, []).append(x)
        if len(buckets[index]) > 50:
            buckets[index] = sorted(buckets[index])
    sorted_arr = []
    for key in sorted(buckets.keys()):
        sorted_arr.extend(sorted(buckets[key]))
    return sorted_arr

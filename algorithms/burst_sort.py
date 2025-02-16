def burst_sort(arr: list) -> list:
    if not arr:
        return arr

    # Determine bucket boundaries.
    # Here we choose a fixed bucket width (tweakable) to simulate bursts.
    bucket_width = 100
    buckets = {}

    # Place each element in a bucket.
    for x in arr:
        # For negative numbers, adjust the bucket index.
        index = (
            (x // bucket_width) if x >= 0 else ((x - bucket_width + 1) // bucket_width)
        )
        if index not in buckets:
            buckets[index] = []
        buckets[index].append(x)
        # "Burst" the bucket if it gets too large.
        if len(buckets[index]) > 50:
            buckets[index] = sorted(buckets[index])

    # Merge the buckets in order.
    sorted_arr = []
    for key in sorted(buckets.keys()):
        # Make sure each bucket is sorted.
        sorted_arr.extend(sorted(buckets[key]))
    return sorted_arr

def spreadsort(arr: list) -> list:
    """
    Spreadsort.

    Time Complexity: Expected O(n)
    Space Complexity: O(n)

    A bucket-based sorting algorithm that first "spreads" the elements into buckets
    based on their normalized value, then sorts each bucket using insertion sort.
    """
    if not arr:
        return arr

    n = len(arr)
    # Determine the minimum and maximum values.
    minimum = arr[0]
    maximum = arr[0]
    for x in arr:
        if x < minimum:
            minimum = x
        if x > maximum:
            maximum = x

    # If all elements are equal, return immediately.
    if minimum == maximum:
        return arr

    # Create buckets. We'll use n buckets.
    buckets = [[] for _ in range(n)]
    range_val = maximum - minimum

    # Distribute elements into buckets.
    for x in arr:
        # Normalize value to a bucket index in [0, n-1]
        index = int(((x - minimum) / range_val) * (n - 1))
        buckets[index].append(x)

    # Insertion sort for each bucket.
    def insertion_sort(bucket):
        for i in range(1, len(bucket)):
            key = bucket[i]
            j = i - 1
            while j >= 0 and bucket[j] > key:
                bucket[j + 1] = bucket[j]
                j -= 1
            bucket[j + 1] = key

    sorted_arr = []
    for bucket in buckets:
        if bucket:
            insertion_sort(bucket)
            sorted_arr.extend(bucket)

    # Copy the sorted result back into the original array.
    for i in range(n):
        arr[i] = sorted_arr[i]
    return arr

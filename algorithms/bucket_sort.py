def bucket_sort(arr: list) -> list:
    """
    Bucket Sort implementation.

    Time Complexity: Average-case O(n + k) where k is the number of buckets; Worst-case O(n²)
    Space Complexity: O(n + k)

    Distributes elements into buckets, sorts each bucket, then concatenates. Works best when data is uniformly distributed.
    """
    if len(arr) == 0:
        return arr
    min_val = min(arr)
    max_val = max(arr)
    bucket_count = len(arr)
    buckets = [[] for _ in range(bucket_count)]

    for num in arr:
        # Compute bucket index (avoid division by zero if all numbers are equal)
        index = (
            (num - min_val) * (bucket_count - 1) // (max_val - min_val)
            if max_val != min_val
            else 0
        )
        buckets[index].append(num)

    sorted_arr = []
    for bucket in buckets:
        sorted_arr.extend(insertion_sort(bucket))
    return sorted_arr


def insertion_sort(arr: list) -> list:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

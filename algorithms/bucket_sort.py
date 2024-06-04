def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

def bucket_sort(arr):
    if len(arr) == 0:
        return arr

    # Determine minimum and maximum values
    min_value, max_value = min(arr), max(arr)

    # Number of buckets
    bucket_count = len(arr)

    # Initialize buckets
    buckets = [[] for _ in range(bucket_count)]

    # Distribute input array values into buckets
    for i in range(len(arr)):
        index = int((arr[i] - min_value) / (max_value - min_value + 1) * bucket_count)
        buckets[index].append(arr[i])

    # Sort individual buckets and concatenate
    sorted_array = []
    for bucket in buckets:
        sorted_array.extend(insertion_sort(bucket))

    return sorted_array
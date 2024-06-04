def flashsort(arr):
    n = len(arr)
    if n == 0:
        return arr

    m = int(0.45 * n)  # Number of classes, can be adjusted

    # Find the minimum and maximum values in the array
    min_val = min(arr)
    max_val = max(arr)
    if min_val == max_val:
        return arr

    # Create the classification array and count elements in each class
    class_counts = [0] * m
    for i in range(n):
        class_index = int((arr[i] - min_val) / (max_val - min_val) * (m - 1))
        class_counts[class_index] += 1

    # Transform class_counts to be the starting index of each class
    for i in range(1, m):
        class_counts[i] += class_counts[i - 1]

    # Permute the elements into the correct classes
    i = 0
    while i < n:
        class_index = int((arr[i] - min_val) / (max_val - min_val) * (m - 1))
        while i >= class_counts[class_index]:
            class_index = int((arr[class_counts[class_index] - 1] - min_val) / (max_val - min_val) * (m - 1))
        while i != class_counts[class_index] - 1:
            correct_class_index = int((arr[i] - min_val) / (max_val - min_val) * (m - 1))
            target_index = class_counts[correct_class_index] - 1
            arr[i], arr[target_index] = arr[target_index], arr[i]
            class_counts[correct_class_index] -= 1
        i += 1

    # Sort each class using insertion sort
    start = 0
    for i in range(m):
        end = class_counts[i]
        if start < end:
            insertion_sort(arr, start, end)
        start = end

    return arr

def insertion_sort(arr, start, end):
    for i in range(start + 1, end):
        key = arr[i]
        j = i - 1
        while j >= start and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
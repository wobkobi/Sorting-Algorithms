def insertion_sort(arr: list) -> list:
    """
    Insertion Sort implementation.

    Time Complexity: Best-case O(n) for nearly sorted data, Worst-case O(n²)
    Space Complexity: O(1)

    Builds the sorted array one element at a time by inserting each new element into its proper place.
    """
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

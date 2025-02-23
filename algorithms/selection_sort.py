def selection_sort(arr: list) -> list:
    """
    Selection Sort implementation.

    Time Complexity: O(n²) in all cases
    Space Complexity: O(1)

    Repeatedly finds the minimum element from the unsorted portion and swaps it with the first unsorted element.
    """
    n = len(arr)
    for i in range(n):
        min_index = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_index]:
                min_index = j
        arr[i], arr[min_index] = arr[min_index], arr[i]
    return arr

def gnome_sort(arr: list) -> list:
    """
    Gnome Sort implementation.

    Time Complexity: O(n²) worst-case
    Space Complexity: O(1)

    Similar to insertion sort but uses a simpler mechanism of swapping elements back until order is restored.
    """
    index = 0
    n = len(arr)
    while index < n:
        if index == 0 or arr[index] >= arr[index - 1]:
            index += 1
        else:
            arr[index], arr[index - 1] = arr[index - 1], arr[index]
            index -= 1
    return arr

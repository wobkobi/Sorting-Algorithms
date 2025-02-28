# cocktail_sort.py
def cocktail_sort(arr):
    """
    Cocktail Sort – a bidirectional variation of bubble sort.

    Time Complexity: Best-case O(n), Worst-case O(n²)
    Space Complexity: O(1)
    """
    if not arr:
        return arr
    n = len(arr)
    start = 0
    end = n - 1
    swapped = True
    while swapped:
        swapped = False
        for i in range(start, end):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        if not swapped:
            break
        swapped = False
        end -= 1
        for i in range(end - 1, start - 1, -1):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                swapped = True
        start += 1
    return arr

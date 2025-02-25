def heap_sort(arr: list) -> list:
    """
    Heap Sort implementation.

    Time Complexity: O(n log n) in all cases
    Space Complexity: O(1) (in-place)

    Converts the list into a heap data structure, then repeatedly extracts the maximum (or minimum) element.
    """
    if not arr:
        return arr

    n = len(arr)
    # Build a max heap.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
    # Extract elements one by one.
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, i, 0)
    return arr


def heapify(arr: list, n: int, i: int):
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[left] > arr[largest]:
        largest = left
    if right < n and arr[right] > arr[largest]:
        largest = right
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def compare_and_swap(arr, i, j, direction):
    if (direction == 1 and arr[i] > arr[j]) or (direction == 0 and arr[i] < arr[j]):
        arr[i], arr[j] = arr[j], arr[i]

def bitonic_merge(arr, low, cnt, direction):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            compare_and_swap(arr, i, i + k, direction)
        bitonic_merge(arr, low, k, direction)
        bitonic_merge(arr, low + k, k, direction)

def bitonic_sort_rec(arr, low, cnt, direction):
    if cnt > 1:
        k = cnt // 2
        bitonic_sort_rec(arr, low, k, 1)      # Ascending
        bitonic_sort_rec(arr, low + k, k, 0)  # Descending
        bitonic_merge(arr, low, cnt, direction)

def bitonic_sort(arr, up=True):
    direction = 1 if up else 0
    bitonic_sort_rec(arr, 0, len(arr), direction)
    return arr
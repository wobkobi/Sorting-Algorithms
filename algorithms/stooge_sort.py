def stooge_sort(arr: list) -> list:
    return stooge_sort_recursive(arr, 0, len(arr) - 1)


def stooge_sort_recursive(arr: list, i: int, j: int) -> list:
    if arr[j] < arr[i]:
        arr[i], arr[j] = arr[j], arr[i]
    if j - i + 1 > 2:
        t = (j - i + 1) // 3
        arr = stooge_sort_recursive(arr, i, j - t)
        arr = stooge_sort_recursive(arr, i + t, j)
        arr = stooge_sort_recursive(arr, i, j - t)
    return arr

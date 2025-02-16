def hyper_quick(arr: list) -> list:
    if len(arr) <= 1:
        return arr
    first, mid, last = arr[0], arr[len(arr) // 2], arr[-1]
    pivot = sorted([first, mid, last])[1]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return hyper_quick(left) + middle + hyper_quick(right)

def spaghetti_sort(arr: list) -> list:
    result = []
    # Remove the maximum repeatedly.
    while arr:
        max_val = max(arr)
        arr.remove(max_val)
        result.append(max_val)
    result.reverse()
    return result

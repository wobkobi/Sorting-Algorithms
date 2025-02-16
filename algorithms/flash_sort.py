def flash_sort(arr: list) -> list:
    n = len(arr)
    if n == 0:
        return arr

    # Shift numbers if negatives exist.
    min_val = min(arr)
    offset = -min_val if min_val < 0 else 0
    if offset:
        arr = [x + offset for x in arr]

    m = max(int(0.43 * n), 1)
    min_val = min(arr)
    max_val = max(arr)
    if min_val == max_val:
        return [x - offset for x in arr]

    # Classify elements.
    c = [0] * m
    for x in arr:
        k = int((m - 1) * (x - min_val) / (max_val - min_val))
        c[k] += 1
    for i in range(1, m):
        c[i] += c[i - 1]
    sorted_arr = [0] * n
    for x in reversed(arr):
        k = int((m - 1) * (x - min_val) / (max_val - min_val))
        c[k] -= 1
        sorted_arr[c[k]] = x
    return [x - offset for x in sorted_arr]

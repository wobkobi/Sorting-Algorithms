# flash_sort.py
def flash_sort(arr):
    """
    Flash Sort – classifies elements into buckets and then sorts within them.

    Time Complexity: Expected O(n) for uniform data; worst-case O(n²)
    Space Complexity: O(n)
    """
    if not arr:
        return []
    n = len(arr)
    min_val = min(arr)
    max_val = max(arr)
    if min_val == max_val:
        return arr[:]
    offset = -min_val if min_val < 0 else 0
    shifted = [x + offset for x in arr]
    m = max(int(0.43 * n), 1)
    min_val, max_val = min(shifted), max(shifted)
    c = [0] * m
    for x in shifted:
        k = int((m - 1) * (x - min_val) / (max_val - min_val))
        c[k] += 1
    for i in range(1, m):
        c[i] += c[i - 1]
    sorted_shifted = [0] * n
    for x in reversed(shifted):
        k = int((m - 1) * (x - min_val) / (max_val - min_val))
        c[k] -= 1
        sorted_shifted[c[k]] = x
    return [x - offset for x in sorted_shifted]

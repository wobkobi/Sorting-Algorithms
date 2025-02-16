def pigeonhole_sort(arr: list) -> list:
    if not arr:
        return arr
    min_val = min(arr)
    max_val = max(arr)
    size = max_val - min_val + 1
    holes = [[] for _ in range(size)]
    for x in arr:
        holes[x - min_val].append(x)
    sorted_arr = []
    for hole in holes:
        sorted_arr.extend(hole)
    return sorted_arr

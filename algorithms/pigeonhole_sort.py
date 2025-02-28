# pigeonhole_sort.py
def pigeonhole_sort(arr):
    """
    Pigeonhole Sort – assigns each element to a “pigeonhole” based on its value.

    Time Complexity: O(n + Range)
    Space Complexity: O(n + Range)
    """
    if not arr:
        return []
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

def pigeonhole_sort(arr: list) -> list:
    """
    Pigeonhole Sort implementation.
    
    Time Complexity: O(n + Range), where Range is the difference between the maximum and minimum values
    Space Complexity: O(n + Range)
    
    Maps each element to a 'pigeonhole' based on its value, then collects the elements in order.
    """
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

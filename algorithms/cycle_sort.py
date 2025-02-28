# cycle_sort.py
def cycle_sort(arr):
    """
    Cycle Sort – minimizes writes by rotating cycles.

    Time Complexity: O(n²)
    Space Complexity: O(1)
    """
    if not arr:
        return []
    a = arr[:]
    n = len(a)
    for cycle_start in range(n - 1):
        item = a[cycle_start]
        pos = cycle_start
        for i in range(cycle_start + 1, n):
            if a[i] < item:
                pos += 1
        if pos == cycle_start:
            continue
        while item == a[pos]:
            pos += 1
        a[pos], item = item, a[pos]
        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, n):
                if a[i] < item:
                    pos += 1
            while item == a[pos]:
                pos += 1
            a[pos], item = item, a[pos]
    return a

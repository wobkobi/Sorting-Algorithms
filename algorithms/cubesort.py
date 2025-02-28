# cubesort.py
import math


def cubesort(arr):
    """
    Cube Sort – arranges elements in a 3D cube, then flattens and sorts.

    Time Complexity: O(n log n) (final sort)
    Space Complexity: O(n)
    """
    if not arr:
        return []
    n = len(arr)
    side = int(n ** (1 / 3))
    if side**3 < n:
        side += 1
    cube = [[[None for _ in range(side)] for _ in range(side)] for _ in range(side)]
    idx = 0
    for i in range(side):
        for j in range(side):
            for k in range(side):
                if idx < n:
                    cube[i][j][k] = arr[idx]
                    idx += 1
    flat = [
        cube[i][j][k]
        for i in range(side)
        for j in range(side)
        for k in range(side)
        if cube[i][j][k] is not None
    ]
    return sorted(flat)

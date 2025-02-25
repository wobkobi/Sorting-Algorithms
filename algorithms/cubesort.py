def cubesort(arr: list) -> list:
    """
    Cube Sort implementation.

    Time Complexity: O(n log n) (due to the use of sorted())
    Space Complexity: O(n) for storing the cube and the flattened list.

    Sorts a list of elements by first arranging them in a 3D cube, then flattening the cube and sorting the flattened list.
    """
    n = len(arr)
    if n <= 1:
        return arr

    # Determine the side length of the cube: smallest integer such that side^3 >= n.
    side = int(n ** (1 / 3))
    if side**3 < n:
        side += 1

    # Initialize a 3D cube (a list of lists of lists) filled with None.
    cube = [[[None for _ in range(side)] for _ in range(side)] for _ in range(side)]

    # Fill the cube with elements from the array.
    idx = 0
    for i in range(side):
        for j in range(side):
            for k in range(side):
                if idx < n:
                    cube[i][j][k] = arr[idx]
                    idx += 1

    # Flatten the cube back into a 1D list, ignoring any None values.
    flat = []
    for i in range(side):
        for j in range(side):
            for k in range(side):
                if cube[i][j][k] is not None:
                    flat.append(cube[i][j][k])

    # Sort the flattened list using Python's built-in sorted() function.
    return sorted(flat)

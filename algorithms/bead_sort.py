def bead_sort(arr: list) -> list:
    """
    Bead Sort implementation.

    Time Complexity: Expected O(n) average-case, Worst-case O(n^2)
    Space Complexity: O(n)

    Simulates gravity on beads arranged on rods. Best for sorting lists of natural numbers.
    """
    if not arr:
        return arr

    # Shift numbers if there are negatives.
    min_val = min(arr)
    shifted = False
    if min_val < 0:
        offset = -min_val
        arr = [x + offset for x in arr]
        shifted = True

    max_beads = max(arr)
    n = len(arr)
    # Create a 2D grid of beads.
    beads = [[1 if j < arr[i] else 0 for j in range(max_beads)] for i in range(n)]
    # Let beads "fall"
    for j in range(max_beads):
        sum_beads = sum(beads[i][j] for i in range(n))
        for i in range(n):
            beads[i][j] = 1 if i >= n - sum_beads else 0
    sorted_arr = [sum(row) for row in beads]

    if shifted:
        sorted_arr = [x - offset for x in sorted_arr]
    return sorted_arr

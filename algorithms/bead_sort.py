# bead_sort.py
def bead_sort(arr):
    """
    Bead Sort – shifts negatives, “drops beads” to count, reconstructs order,
    then undoes the shift.

    Time Complexity: O(n * (max(arr)-min(arr)))
    Space Complexity: O(n + (max(arr)-min(arr)))
    """
    if not arr:
        return []
    min_val = min(arr)
    shift = -min_val if min_val < 0 else 0
    shifted = [x + shift for x in arr]
    max_val = max(shifted)
    beads = [0] * max_val
    for num in shifted:
        for j in range(num):
            beads[j] += 1
    n = len(shifted)
    sorted_desc = [sum(1 for bead in beads if bead > i) for i in range(n)]
    sorted_arr = sorted_desc[::-1]
    return [x - shift for x in sorted_arr]

def bead_sort(arr: list) -> list:
    """
    Optimized Bead Sort implementation that reduces memory usage by avoiding
    the construction of a full 2D grid. This version supports all integers
    (including negative numbers) by shifting the input so that all numbers are non-negative,
    sorting the shifted values, and then undoing the shift.

    Time Complexity: O(n * (max(arr) - min(arr)))
    Space Complexity: O(n + (max(arr) - min(arr)))
    """
    if not arr:
        return arr

    # Determine the shift to apply if there are negative numbers.
    min_val = min(arr)
    shift = -min_val if min_val < 0 else 0
    shifted_arr = [x + shift for x in arr]

    max_val = max(shifted_arr)
    # Create a beads list to count beads in each "column"
    beads = [0] * max_val

    # Simulate dropping beads for each number in the shifted array.
    for number in shifted_arr:
        for j in range(number):
            beads[j] += 1

    # Reconstruct the sorted (in descending order) shifted array.
    n = len(shifted_arr)
    sorted_desc = []
    for i in range(n):
        row_count = sum(1 for count in beads if count > i)
        sorted_desc.append(row_count)

    # Reverse to obtain ascending order and then undo the shift.
    sorted_shifted = sorted_desc[::-1]
    return [x - shift for x in sorted_shifted]

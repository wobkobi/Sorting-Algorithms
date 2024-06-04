def gravity_sort(arr):
    if any(not isinstance(x, int) or x < 0 for x in arr):
        raise ValueError("All elements must be non-negative integers")

    if not arr:
        return arr

    max_element = max(arr)
    beads = [[0] * len(arr) for _ in range(max_element)]

    # Place beads
    for i, num in enumerate(arr):
        for j in range(num):
            beads[j][i] = 1

    # Let beads fall
    for row in beads:
        count = sum(row)
        for j in range(len(arr) - count):
            row[j] = 0
        for j in range(len(arr) - count, len(arr)):
            row[j] = 1

    # Write output
    for i in range(len(arr)):
        arr[i] = sum(beads[j][i] for j in range(max_element))

    return arr
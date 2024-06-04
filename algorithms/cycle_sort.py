def cycle_sort(arr):
    writes = 0

    # Loop through the array to find cycles to rotate.
    for cycle_start in range(0, len(arr) - 1):
        item = arr[cycle_start]

        # Find where to place the item.
        pos = cycle_start
        for i in range(cycle_start + 1, len(arr)):
            if arr[i] < item:
                pos += 1

        # If the item is already in the correct position, continue.
        if pos == cycle_start:
            continue

        # Otherwise, put the item in its correct position.
        while item == arr[pos]:
            pos += 1
        arr[pos], item = item, arr[pos]
        writes += 1

        # Rotate the rest of the cycle.
        while pos != cycle_start:
            pos = cycle_start
            for i in range(cycle_start + 1, len(arr)):
                if arr[i] < item:
                    pos += 1
            while item == arr[pos]:
                pos += 1
            arr[pos], item = item, arr[pos]
            writes += 1

    return arr
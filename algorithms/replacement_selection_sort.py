import heapq
from heapq import merge


def replacement_selection_sort(arr: list) -> list:
    if not arr:
        return arr

    runs = []
    remaining = arr[:]  # copy of the array

    while remaining:
        heap = []
        run = []
        # Build initial heap from the remaining elements.
        for x in remaining:
            heap.append(x)
        heapq.heapify(heap)
        new_remaining = []
        last_output = -float("inf")
        while heap:
            x = heapq.heappop(heap)
            if x >= last_output:
                run.append(x)
                last_output = x
            else:
                new_remaining.append(x)
        runs.append(run)
        remaining = new_remaining

    # Merge all runs using a k-way merge.
    result = []
    for run in runs:
        result = list(merge(result, run))
    return result

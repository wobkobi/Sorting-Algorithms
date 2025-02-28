# replacement_selection_sort.py
import heapq
from heapq import merge


def replacement_selection_sort(arr):
    """
    Replacement Selection Sort – builds initial runs with a heap, then merges them.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if not arr:
        return []
    runs = []
    remaining = arr[:]
    while remaining:
        heap = remaining[:]
        heapq.heapify(heap)
        run = []
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
    result = []
    for run in runs:
        result = list(merge(result, run))
    return result

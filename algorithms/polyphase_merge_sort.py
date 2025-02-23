import heapq


def polyphase_merge_sort(arr: list) -> list:
    """
    Polyphase Merge Sort implementation.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n)
    
    An external sorting algorithm that minimizes the number of merge passes using an uneven distribution of runs.
    """
    if not arr:
        return arr

    # Phase 1: Generate runs.
    runs = []
    current_run = [arr[0]]
    for x in arr[1:]:
        if x >= current_run[-1]:
            current_run.append(x)
        else:
            runs.append(current_run)
            current_run = [x]
    runs.append(current_run)

    # Phase 2: Merge the runs using a k‑way merge.
    heap = []
    # Build an initial heap entry for each run.
    for run_idx, run in enumerate(runs):
        if run:
            heapq.heappush(heap, (run[0], run_idx, 0))
    result = []
    while heap:
        val, run_idx, idx_in_run = heapq.heappop(heap)
        result.append(val)
        if idx_in_run + 1 < len(runs[run_idx]):
            heapq.heappush(
                heap, (runs[run_idx][idx_in_run + 1], run_idx, idx_in_run + 1)
            )
    return result

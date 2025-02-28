# polyphase_merge_sort.py
import heapq


def polyphase_merge_sort(arr):
    """
    Polyphase Merge Sort – minimizes merge passes using an uneven run distribution.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if not arr:
        return []
    runs = []
    current_run = [arr[0]]
    for x in arr[1:]:
        if x >= current_run[-1]:
            current_run.append(x)
        else:
            runs.append(current_run)
            current_run = [x]
    runs.append(current_run)
    heap = []
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

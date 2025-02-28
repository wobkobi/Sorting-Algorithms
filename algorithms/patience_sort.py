# patience_sort.py
import heapq


def patience_sort(arr):
    """
    Patience Sort – builds piles (like in the card game) and merges them.

    Time Complexity: O(n log n)
    Space Complexity: O(n)
    """
    if not arr:
        return []
    piles = []
    for x in arr:
        placed = False
        for pile in piles:
            if x < pile[-1]:
                pile.append(x)
                placed = True
                break
        if not placed:
            piles.append([x])
    for pile in piles:
        pile.reverse()
    heap = []
    for i, pile in enumerate(piles):
        heapq.heappush(heap, (pile[0], i, 0))
    result = []
    while heap:
        val, i, idx = heapq.heappop(heap)
        result.append(val)
        if idx + 1 < len(piles[i]):
            heapq.heappush(heap, (piles[i][idx + 1], i, idx + 1))
    return result

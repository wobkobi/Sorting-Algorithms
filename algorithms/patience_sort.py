def patience_sort(arr: list) -> list:
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
    # Reverse each pile so that the smallest element is first.
    for pile in piles:
        pile.reverse()
    # Merge piles using a simple k‑way merge.
    import heapq

    heap = []
    for i, pile in enumerate(piles):
        heap.append((pile[0], i, 0))
    heapq.heapify(heap)
    result = []
    while heap:
        val, i, idx = heapq.heappop(heap)
        result.append(val)
        if idx + 1 < len(piles[i]):
            heapq.heappush(heap, (piles[i][idx + 1], i, idx + 1))
    return result

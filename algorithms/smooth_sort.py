def smooth_sort(arr: list) -> list:
    n = len(arr)
    if n < 2:
        return arr

    # Returns the Leonardo number L(order)
    def leo_value(order: int) -> int:
        if order < 2:
            return 1
        a, b = 1, 1
        for _ in range(2, order + 1):
            a, b = b, a + b + 1
        return b

    # Sift the element at index i down a Leonardo heap of given order.
    def sift(i: int, order: int):
        while order >= 2:
            r = i - 1
            l = i - 1 - leo_value(order - 2)
            if l < 0 or r < 0:
                break
            if arr[l] >= arr[r]:
                child = l
                new_order = order - 1
            else:
                child = r
                new_order = order - 2
            if arr[i] >= arr[child]:
                break
            arr[i], arr[child] = arr[child], arr[i]
            i = child
            order = new_order

    # "Trinkle" operation: restore heap order for element at index i.
    def trinkle(i: int, p: int, order: int):
        while p:
            j = i - leo_value(order)
            if j < 0 or j >= n:
                break
            if arr[j] <= arr[i]:
                break
            arr[i], arr[j] = arr[j], arr[i]
            i = j
            p //= 2
            order -= 1

    # Build the heap forest.
    p = 1
    leo = []
    for i in range(n):
        leo.append(1)
        p = (p << 1) | 1
        while len(leo) >= 2 and leo[-2] == leo[-1] + 1:
            leo[-2] += 1
            leo.pop()
            p //= 2
        trinkle(i, p, leo[-1])

    # Sort phase: extract the maximum element repeatedly.
    for i in range(n - 1, -1, -1):
        if leo:
            order = leo.pop()
            p //= 2
            if order >= 2:
                left = i - leo_value(order)
                right = i - 1
                leo.append(order - 1)
                p = (p << 1) | 1
                trinkle(left, p, order - 1)
                leo.append(order - 2)
                p = (p << 1) | 1
                trinkle(right, p, order - 2)
    return arr

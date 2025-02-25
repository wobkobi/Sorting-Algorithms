def smooth_sort(arr: list) -> list:
    """
    Smooth Sort implementation.

    Time Complexity: Worst-case O(n log n), Best-case O(n) for nearly sorted data
    Space Complexity: O(1)

    A variation of heap sort that adapts to the existing order in the input, potentially offering faster performance on nearly sorted lists.
    """
    if not arr:
        return arr

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
        root = arr[i]
        while order >= 2:
            right = i - 1
            left = i - 1 - leo_value(order - 2)
            # Choose the larger child.
            if arr[left] >= arr[right]:
                child = left
                new_order = order - 1
            else:
                child = right
                new_order = order - 2
            if root >= arr[child]:
                break
            arr[i] = arr[child]
            i = child
            order = new_order
        arr[i] = root

    # "Trinkle" operation: restore heap order for element at index i.
    def trinkle(i: int, p: int, order: int):
        root = arr[i]
        while p:
            # Shift p until its least-significant bit is 1.
            while p % 2 == 0:
                p //= 2
                order += 1
            j = i - leo_value(order)
            if j < 0 or arr[j] <= root:
                break
            arr[i] = arr[j]
            i = j
            p //= 2
            order -= 1
        arr[i] = root
        sift(i, order)

    # Build the heap forest.
    p = 1
    leo_stack = []
    for i in range(n):
        leo_stack.append(1)
        p = (p << 1) | 1
        # Merge adjacent trees if they are consecutive in order.
        while len(leo_stack) >= 2 and leo_stack[-2] == leo_stack[-1] + 1:
            leo_stack[-2] += 1
            leo_stack.pop()
            p //= 2
        trinkle(i, p, leo_stack[-1])

    # Sort phase: extract the maximum element repeatedly.
    for i in range(n - 1, -1, -1):
        if leo_stack:
            order = leo_stack.pop()
            p //= 2
            if order >= 2:
                # When splitting a heap of order 'order', its two subheaps have orders:
                #   order - 1 and order - 2.
                # Their roots are at:
                #   left: i - 1 - leo_value(order - 2)
                #   right: i - 1
                left = i - 1 - leo_value(order - 2)
                right = i - 1
                leo_stack.append(order - 1)
                p = (p << 1) | 1
                trinkle(left, p, order - 1)
                leo_stack.append(order - 2)
                p = (p << 1) | 1
                trinkle(right, p, order - 2)
    return arr

# smooth_sort.py
import math


def smooth_sort(arr):
    """
    Smooth Sort – adapts to the existing order in the list.

    Time Complexity: Worst-case O(n log n), best-case O(n) for nearly sorted data.
    Space Complexity: O(1)
    """
    if not arr:
        return []
    a = arr[:]
    n = len(a)
    if n < 2:
        return a

    def leo_value(order):
        if order < 2:
            return 1
        a_val, b_val = 1, 1
        for _ in range(2, order + 1):
            a_val, b_val = b_val, a_val + b_val + 1
        return b_val

    def sift(i, order):
        root = a[i]
        while order >= 2:
            right = i - 1
            left = i - 1 - leo_value(order - 2)
            if a[left] >= a[right]:
                child = left
                new_order = order - 1
            else:
                child = right
                new_order = order - 2
            if root >= a[child]:
                break
            a[i] = a[child]
            i = child
            order = new_order
        a[i] = root

    def trinkle(i, p, order):
        root = a[i]
        while p:
            while p % 2 == 0:
                p //= 2
                order += 1
            j = i - leo_value(order)
            if j < 0 or a[j] <= root:
                break
            a[i] = a[j]
            i = j
            p //= 2
            order -= 1
        a[i] = root
        sift(i, order)

    p = 1
    leo_stack = []
    for i in range(n):
        leo_stack.append(1)
        p = (p << 1) | 1
        while len(leo_stack) >= 2 and leo_stack[-2] == leo_stack[-1] + 1:
            leo_stack[-2] += 1
            leo_stack.pop()
            p //= 2
        trinkle(i, p, leo_stack[-1])

    for i in range(n - 1, -1, -1):
        if leo_stack:
            order = leo_stack.pop()
            p //= 2
            if order >= 2:
                left = i - 1 - leo_value(order - 2)
                right = i - 1
                leo_stack.append(order - 1)
                p = (p << 1) | 1
                trinkle(left, p, order - 1)
                leo_stack.append(order - 2)
                p = (p << 1) | 1
                trinkle(right, p, order - 2)
    return a

import math


def intro_sort(arr: list) -> list:
    maxdepth = math.floor(math.log2(len(arr))) * 2 if arr else 0

    def _introsort(a, start, end, depth):
        if end - start <= 1:
            return
        if depth == 0:
            heap_sort_slice(a, start, end)
        else:
            pivot = partition(a, start, end)
            _introsort(a, start, pivot, depth - 1)
            _introsort(a, pivot + 1, end, depth - 1)

    def partition(a, low, high):
        pivot = a[high - 1]
        i = low
        for j in range(low, high - 1):
            if a[j] <= pivot:
                a[i], a[j] = a[j], a[i]
                i += 1
        a[i], a[high - 1] = a[high - 1], a[i]
        return i

    def heap_sort_slice(a, start, end):
        def heapify(a, count, i, offset):
            largest = i
            left = 2 * i + 1
            right = 2 * i + 2
            if left < count and a[offset + left] > a[offset + largest]:
                largest = left
            if right < count and a[offset + right] > a[offset + largest]:
                largest = right
            if largest != i:
                a[offset + i], a[offset + largest] = a[offset + largest], a[offset + i]
                heapify(a, count, largest, offset)

        count = end - start
        for i in range(count // 2 - 1, -1, -1):
            heapify(a, count, i, start)
        for i in range(count - 1, 0, -1):
            a[start], a[start + i] = a[start + i], a[start]
            heapify(a, i, 0, start)

    _introsort(arr, 0, len(arr), maxdepth)
    return arr

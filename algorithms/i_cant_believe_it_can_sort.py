# i_cant_believe_it_can_sort.py
def i_cant_believe_it_can_sort(arr):
    """
    I Can't Believe It Can Sort – a recursive merge-style sort.

    Time Complexity: Average O(n log n)
    Space Complexity: O(n)
    """
    if not arr:
        return []
    if len(arr) <= 1:
        return arr[:]
    mid = len(arr) // 2
    left = i_cant_believe_it_can_sort(arr[:mid])
    right = i_cant_believe_it_can_sort(arr[mid:])
    i = j = 0
    merged = []
    while i < len(left) and j < len(right):
        if left[i] < right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged

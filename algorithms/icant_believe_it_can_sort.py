def icant_believe_it_can_sort(arr: list) -> list:
    """
    I Can't Believe It Can Sort.

    Time Complexity: O(n log n) on average
    Space Complexity: O(n)

    An intentionally over-engineered recursive sort that merges the array in a surprising way.
    """
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = icant_believe_it_can_sort(arr[:mid])
    right = icant_believe_it_can_sort(arr[mid:])
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
    arr[:] = merged
    return arr

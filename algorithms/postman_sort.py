def postman_sort(arr: list) -> list:
    """
    Postman Sort implementation.

    Time Complexity: Expected O(n log n)
    Space Complexity: O(n)

    A lesser-known method that uses a multi-phase merging or message-passing strategy. Details may vary with implementation.
    """
    if not arr:
        return arr

    # Separate negatives and non-negatives.
    negatives = [-x for x in arr if x < 0]
    non_negatives = [x for x in arr if x >= 0]

    sorted_negatives = lsd_radix_sort(negatives)
    sorted_non_negatives = lsd_radix_sort(non_negatives)

    # Reverse negatives (to restore correct order) and merge.
    return [-x for x in sorted_negatives][::-1] + sorted_non_negatives


def lsd_radix_sort(arr: list) -> list:
    if not arr:
        return arr
    max_val = max(arr)
    exp = 1
    while max_val // exp > 0:
        arr = counting_sort_for_radix(arr, exp)
        exp *= 10
    return arr


def counting_sort_for_radix(arr: list, exp: int) -> list:
    n = len(arr)
    output = [0] * n
    count = [0] * 10
    for x in arr:
        index = (x // exp) % 10
        count[index] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    return output

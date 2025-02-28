# radix_sort.py
def counting_sort_for_radix(arr, exp):
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


def radix_sort(arr):
    """
    Radix Sort (LSD) – processes digits from least significant to most.

    Time Complexity: O(nk) where k is number of digits.
    Space Complexity: O(n + k)
    """
    if not arr:
        return []
    max_val = max(arr)
    exp = 1
    a = arr[:]
    while max_val // exp > 0:
        a = counting_sort_for_radix(a, exp)
        exp *= 10
    return a

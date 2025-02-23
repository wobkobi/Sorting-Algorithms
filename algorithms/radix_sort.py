def radix_sort(arr: list) -> list:
    """
    Radix Sort implementation.

    Time Complexity: O(nk) where k is the number of digits or characters in the keys
    Space Complexity: O(n + k)

    A non-comparative sort that processes the input digit by digit (or character by character), often using counting sort as a subroutine.
    """
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
    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1
    for i in range(1, 10):
        count[i] += count[i - 1]
    for i in range(n - 1, -1, -1):
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
    return output

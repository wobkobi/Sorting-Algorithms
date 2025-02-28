# counting_sort.py
def counting_sort(arr):
    """
    Counting Sort – non-comparative sort for integers.

    Time Complexity: O(n + k) where k is the range of input.
    Space Complexity: O(n + k)
    """
    if not arr:
        return []
    min_val = min(arr)
    max_val = max(arr)
    range_of_elements = max_val - min_val + 1
    count = [0] * range_of_elements
    output = [0] * len(arr)
    for num in arr:
        count[num - min_val] += 1
    for i in range(1, len(count)):
        count[i] += count[i - 1]
    for num in reversed(arr):
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1
    return output

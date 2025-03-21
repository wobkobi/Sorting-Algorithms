# lsd_radix_sort.py
def lsd_radix_sort(arr):
    """
    LSD Radix Sort implementation.

    Time Complexity: O(d * (n + k)), where d is the number of digits and k is the range of digit values.
    Space Complexity: O(n + k)

    This implementation sorts the array using the least-significant-digit radix sort algorithm.
    """
    if not arr:
        return []

    negatives = [x for x in arr if x < 0]
    non_negatives = [x for x in arr if x >= 0]

    def lsd_sort(nums):
        # Standard LSD Radix Sort for non-negative integers.
        if not nums:
            return nums
        max_num = max(nums)
        exp = 1
        n = len(nums)
        output = [0] * n
        while max_num // exp > 0:
            count = [0] * 10
            for num in nums:
                index = (num // exp) % 10
                count[index] += 1
            for i in range(1, 10):
                count[i] += count[i - 1]
            for i in range(n - 1, -1, -1):
                index = (nums[i] // exp) % 10
                output[count[index] - 1] = nums[i]
                count[index] -= 1
            nums = output[:]  # copy output to nums for next digit
            exp *= 10
        return nums

    sorted_non_neg = lsd_sort(non_negatives)

    if negatives:
        abs_negatives = [abs(x) for x in negatives]
        sorted_abs_neg = lsd_sort(abs_negatives)
        sorted_negatives = [-x for x in sorted_abs_neg[::-1]]
    else:
        sorted_negatives = []

    return sorted_negatives + sorted_non_neg

def lsd_radix_sort(arr: list) -> list:
    """
    LSD Radix Sort implementation for non-negative integers.

    Time Complexity: O(d * (n + k)), where d is the number of digits and k is the range of digit values.
    Space Complexity: O(n + k)

    This implementation sorts the array using the least-significant-digit radix sort algorithm.
    It assumes that the input consists of non-negative integers.
    """
    if not arr:
        return arr

    # Find the maximum number to determine the number of digits.
    max_num = max(arr)
    exp = 1  # Exponent corresponding to the current digit position.
    n = len(arr)
    output = [0] * n

    # Process each digit position.
    while max_num // exp > 0:
        count = [0] * 10

        # Count occurrences of each digit.
        for i in range(n):
            index = (arr[i] // exp) % 10
            count[index] += 1

        # Modify count so that it contains actual positions.
        for i in range(1, 10):
            count[i] += count[i - 1]

        # Build the output array using a stable sort.
        for i in range(n - 1, -1, -1):
            index = (arr[i] // exp) % 10
            output[count[index] - 1] = arr[i]
            count[index] -= 1

        # Copy the output array to arr.
        for i in range(n):
            arr[i] = output[i]

        exp *= 10

    return arr

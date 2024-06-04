def counting_sort(arr):
    if len(arr) == 0:
        return arr

    # Find the maximum and minimum values in the array
    max_val = max(arr)
    min_val = min(arr)

    # Range of the numbers in the array
    range_of_elements = max_val - min_val + 1

    # Create a count array to store the count of each unique object
    count = [0] * range_of_elements

    # Store the count of each element in the count array
    for num in arr:
        count[num - min_val] += 1

    # Modify the count array such that each element at each index
    # stores the sum of previous counts
    for i in range(1, len(count)):
        count[i] += count[i - 1]

    # Output array to store the sorted elements
    output = [0] * len(arr)

    # Build the output array
    for num in reversed(arr):
        output[count[num - min_val] - 1] = num
        count[num - min_val] -= 1

    return output
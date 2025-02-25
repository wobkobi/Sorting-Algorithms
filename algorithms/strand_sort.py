def strand_sort(arr: list) -> list:
    """
    Strand Sort implementation.

    Time Complexity: Worst-case O(n²); may perform better on partially sorted data
    Space Complexity: O(n)

    Repeatedly extracts increasing subsequences (strands) from the list and merges them to form the sorted output.
    """

    def merge_strands(a: list, b: list) -> list:
        result = []
        i = j = 0
        while i < len(a) and j < len(b):
            if a[i] <= b[j]:
                result.append(a[i])
                i += 1
            else:
                result.append(b[j])
                j += 1
        result.extend(a[i:])
        result.extend(b[j:])
        return result

    if not arr:
        return arr

    output = []

    while arr:
        # Build a strand.
        strand = [arr.pop(0)]
        i = 0
        while i < len(arr):
            if arr[i] >= strand[-1]:
                strand.append(arr.pop(i))
            else:
                i += 1
        output = merge_strands(output, strand)
    return output

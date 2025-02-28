# strand_sort.py
def strand_sort(arr):
    """
    Strand Sort – repeatedly extracts increasing subsequences (“strands”) and merges them.

    Time Complexity: Worst-case O(n²), but can perform better on partially sorted data.
    Space Complexity: O(n)
    """
    if not arr:
        return []

    def merge_strands(a, b):
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

    output = []
    a = arr[:]
    while a:
        strand = [a.pop(0)]
        i = 0
        while i < len(a):
            if a[i] >= strand[-1]:
                strand.append(a.pop(i))
            else:
                i += 1
        output = merge_strands(output, strand) if output else strand
    return output

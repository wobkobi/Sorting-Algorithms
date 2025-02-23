from heapq import merge


def external_merge_sort(arr: list) -> list:
    """
    External Merge Sort implementation.
    
    Time Complexity: O(n log n)
    Space Complexity: O(n) (external storage required)
    
    Designed for sorting data too large to fit in memory by merging sorted runs stored externally.
    """
    if len(arr) <= 1:
        return arr
    chunk_size = 1000  # Simulated chunk size.
    chunks = [sorted(arr[i : i + chunk_size]) for i in range(0, len(arr), chunk_size)]
    result = []
    for chunk in chunks:
        result = list(merge(result, chunk))
    return result

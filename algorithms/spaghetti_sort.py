def spaghetti_sort(arr: list) -> list:
    """
    Spaghetti Sort implementation.

    Time Complexity: Conceptually O(n) when using physical analogies, but not practical in software
    Space Complexity: O(n)

    A non-comparative sort that mimics aligning strands of spaghetti to determine order. Mostly used as a conceptual or humorous algorithm.
    """
    if not arr:
        return arr

    result = []
    # Remove the maximum repeatedly.
    while arr:
        max_val = max(arr)
        arr.remove(max_val)
        result.append(max_val)
    result.reverse()
    return result

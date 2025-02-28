# spaghetti_sort.py
def spaghetti_sort(arr):
    """
    Spaghetti Sort – repeatedly removes the maximum element.

    Time Complexity: Conceptually O(n) (impractical in software).
    Space Complexity: O(n)
    """
    if not arr:
        return []
    a = arr[:]
    result = []
    while a:
        max_val = max(a)
        a.remove(max_val)
        result.append(max_val)
    result.reverse()
    return result

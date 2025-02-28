# gnome_sort.py
def gnome_sort(arr):
    """
    Gnome Sort – moves elements back one step at a time until order is restored.

    Time Complexity: O(n²) worst-case
    Space Complexity: O(1)
    """
    if not arr:
        return []
    a = arr[:]
    i = 0
    n = len(a)
    while i < n:
        if i == 0 or a[i] >= a[i - 1]:
            i += 1
        else:
            a[i], a[i - 1] = a[i - 1], a[i]
            i -= 1
    return a

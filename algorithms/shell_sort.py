def shell_sort(arr: list) -> list:
    """
    Shell Sort implementation.
    
    Time Complexity: Varies between O(n log² n) and O(n^(3/2)) depending on the gap sequence
    Space Complexity: O(1)
    
    An optimization over insertion sort that allows elements to move farther in each pass by using gaps.
    """
    n = len(arr)
    gap = n // 2
    while gap > 0:
        for i in range(gap, n):
            temp = arr[i]
            j = i
            while j >= gap and arr[j - gap] > temp:
                arr[j] = arr[j - gap]
                j -= gap
            arr[j] = temp
        gap //= 2
    return arr

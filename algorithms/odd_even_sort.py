def odd_even_sort(arr: list) -> list:
    """
    Odd-Even Sort implementation.
    
    Time Complexity: O(n²) worst-case
    Space Complexity: O(1)
    
    Alternates between comparing odd-indexed and even-indexed pairs. Simple but not efficient on large arrays.
    """
    n = len(arr)
    sorted_flag = False
    while not sorted_flag:
        sorted_flag = True
        # Compare odd indexed pairs.
        for i in range(1, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted_flag = False
        # Compare even indexed pairs.
        for i in range(0, n - 1, 2):
            if arr[i] > arr[i + 1]:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]
                sorted_flag = False
    return arr

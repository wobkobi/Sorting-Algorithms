def counting_sort(arr: list) -> list:
    if not arr:
        return arr
    max_val = max(arr)
    count = [0] * (max_val + 1)
    for num in arr:
        count[num] += 1
    index = 0
    for i, cnt in enumerate(count):
        for _ in range(cnt):
            arr[index] = i
            index += 1
    return arr

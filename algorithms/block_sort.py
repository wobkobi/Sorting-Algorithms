def merge(left, right):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def block_sort(arr, block_size=64):
    n = len(arr)
    if n <= block_size:
        return sorted(arr)

    # Divide the array into blocks and sort each block
    blocks = [sorted(arr[i:i+block_size]) for i in range(0, n, block_size)]

    # Merge the blocks
    while len(blocks) > 1:
        merged_blocks = []
        for i in range(0, len(blocks) - 1, 2):
            merged_blocks.append(merge(blocks[i], blocks[i + 1]))
        if len(blocks) % 2 == 1:
            merged_blocks.append(blocks[-1])
        blocks = merged_blocks

    return blocks[0]
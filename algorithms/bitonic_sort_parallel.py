import multiprocessing as mp

def compare_and_swap(arr, i, j, direction):
    if (direction == 1 and arr[i] > arr[j]) or (direction == 0 and arr[i] < arr[j]):
        arr[i], arr[j] = arr[j], arr[i]

def bitonic_merge(arr, low, cnt, direction):
    if cnt > 1:
        k = cnt // 2
        for i in range(low, low + k):
            compare_and_swap(arr, i, i + k, direction)
        bitonic_merge(arr, low, k, direction)
        bitonic_merge(arr, low + k, k, direction)

def bitonic_sort_rec(arr, low, cnt, direction):
    if cnt > 1:
        k = cnt // 2
        bitonic_sort_rec(arr, low, k, 1)      # Ascending
        bitonic_sort_rec(arr, low + k, k, 0)  # Descending
        bitonic_merge(arr, low, cnt, direction)

def bitonic_sort(arr, up=True):
    direction = 1 if up else 0
    bitonic_sort_rec(arr, 0, len(arr), direction)
    return arr

def parallel_bitonic_sort(arr, up=True):
    num_threads = mp.cpu_count()
    pool = mp.Pool(processes=num_threads)
    size = len(arr)

    direction = 1 if up else 0

    def parallel_sort(start, length):
        bitonic_sort_rec(arr, start, length, direction)

    chunk_size = size // num_threads
    tasks = [(i * chunk_size, chunk_size) for i in range(num_threads)]

    if size % num_threads != 0:
        tasks[-1] = (tasks[-1][0], size - tasks[-1][0])

    pool.starmap(parallel_sort, tasks)
    pool.close()
    pool.join()

    bitonic_merge(arr, 0, size, direction)
    return arr
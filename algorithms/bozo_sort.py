import random

def is_sorted(arr):
    for i in range(len(arr) - 1):
        if arr[i] > arr[i + 1]:
            return False
    return True

def bozo_sort(arr):
    attempts = 0
    while not is_sorted(arr):
        i, j = random.randint(0, len(arr) - 1), random.randint(0, len(arr) - 1)
        arr[i], arr[j] = arr[j], arr[i]
        attempts += 1
    print(f"Sorted after {attempts} attempts.")
    return arr
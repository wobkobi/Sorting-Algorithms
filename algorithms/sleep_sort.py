import threading
import time


def sleep_sort(arr: list) -> list:
    if not arr:
        return arr

    # Shift numbers if there are negatives.
    min_val = min(arr)
    offset = -min_val if min_val < 0 else 0

    result = []
    threads = []

    def worker(x):
        # Sleep time based on shifted value.
        time.sleep((x + offset) / 1000000.0)
        result.append(x)

    for x in arr:
        thread = threading.Thread(target=worker, args=(x,))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return result

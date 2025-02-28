# sleep_sort.py
import threading
import time


def sleep_sort(arr):
    """
    Sleep Sort – uses thread sleep delays based on element values.

    (A novelty algorithm; not for production use.)

    Time Complexity: Conceptually O(n), but overhead makes it impractical.
    Space Complexity: O(n)
    """
    if not arr:
        return []
    min_val = min(arr)
    offset = -min_val if min_val < 0 else 0
    result = []
    threads = []
    lock = threading.Lock()

    def worker(x):
        time.sleep((x + offset) / 1000000.0)
        with lock:
            result.append(x)

    for x in arr:
        t = threading.Thread(target=worker, args=(x,))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return result

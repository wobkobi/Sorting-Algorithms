from .radix_sort import radix_sort


def postman_sort(arr):
    if not arr:
        return []
    negatives = [-x for x in arr if x < 0]
    non_negatives = [x for x in arr if x >= 0]
    sorted_negatives = radix_sort(negatives)
    sorted_non_negatives = radix_sort(non_negatives)
    return ([-x for x in sorted_negatives][::-1]) + sorted_non_negatives

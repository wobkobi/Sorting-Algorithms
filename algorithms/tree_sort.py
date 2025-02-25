class Node:
    def __init__(self, key):
        self.left = None
        self.right = None
        self.key = key


def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    return root


def inorder(root, arr):
    if root is not None:
        inorder(root.left, arr)
        arr.append(root.key)
        inorder(root.right, arr)


def tree_sort(arr: list) -> list:
    """
    Tree Sort implementation.

    Time Complexity: Average-case O(n log n), Worst-case O(n²) if the tree becomes unbalanced
    Space Complexity: O(n)

    Inserts elements into a binary search tree and then performs an in-order traversal to yield a sorted list.
    """
    if not arr:
        return arr

    root = None
    for num in arr:
        root = insert(root, num)
    sorted_arr = []
    inorder(root, sorted_arr)
    return sorted_arr

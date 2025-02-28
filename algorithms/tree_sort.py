# tree_sort.py
class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None


def insert(root, key):
    if root is None:
        return Node(key)
    if key < root.key:
        root.left = insert(root.left, key)
    else:
        root.right = insert(root.right, key)
    return root


def inorder(root, res):
    if root is not None:
        inorder(root.left, res)
        res.append(root.key)
        inorder(root.right, res)


def tree_sort(arr):
    """
    Tree Sort – inserts elements into a binary search tree and performs an in-order traversal.

    Time Complexity: Average O(n log n), worst-case O(n²) if unbalanced.
    Space Complexity: O(n)
    """
    if not arr:
        return []
    root = None
    for num in arr:
        root = insert(root, num)
    result = []
    inorder(root, result)
    return result

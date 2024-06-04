class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_string = False

class BurstTrie:
    def __init__(self):
        self.root = TrieNode()
        self.buckets = []

    def insert(self, string):
        node = self.root
        for char in string:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_string = True

    def collect(self, node=None, prefix="", result=None):
        if result is None:
            result = []
        if node is None:
            node = self.root

        if node.is_end_of_string:
            result.append(prefix)

        for char, child in node.children.items():
            self.collect(child, prefix + char, result)

        return result

def burst_sort(arr):
    if not arr:
        return arr

    trie = BurstTrie()
    for string in arr:
        trie.insert(string)

    return trie.collect()

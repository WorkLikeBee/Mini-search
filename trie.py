from trie_node import TrieNode

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        current = self.root
        for letter in word:
            if letter not in current.children:
                current.children[letter] = TrieNode()
            current = current.children[letter]

        current.is_end_of_word = True 

    def autocomplete(self, prefix):
        current = self.root
        prefix = prefix.lower().strip()
        for letter in prefix:
            if letter not in current.children:
                return [] #no word starts with this prefix
            current = current.children[letter]
        results = []
        self._collect(current, prefix, results)
        return sorted(results)

    #recursive call
    def _collect(self, node, prefix, results):
        """
        Add every complete word below node to results, using DFS (Depth-first search)
        """
        if node.is_end_of_word:
            results.append(prefix)

        for letter, child in node.children.items():
            self._collect(child, prefix + letter, results)


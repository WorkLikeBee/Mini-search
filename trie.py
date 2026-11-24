from trie_node import TrieNode
from tokenizer import tokenize
from index import search_query

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

    def autocomplete(self, prefix, limit=10, is_valid=None):
        current = self.root
        prefix = prefix.lower().strip()
        for letter in prefix:
            if letter not in current.children:
                return [] #no word starts with this prefix
            current = current.children[letter]
        results = []
        self._collect(current, prefix, results, limit, is_valid)

        return results

    #recursive call
    def _collect(self, node, prefix, results, limit, is_valid):
        """
        Add every complete word below node to results, using DFS (Depth-first search)
        """
        if len(results) >= limit:
            return
        if node.is_end_of_word and (is_valid is None or is_valid(prefix)):
            results.append(prefix)

        for letter, child in sorted(node.children.items()):
            self._collect(child, prefix + letter, results, limit, is_valid)
            if len(results) >= limit:
                return

def complete_query(query, trie, index, limit=10):
    """Autocomplete the last word of a query, keeping the earlier words."""
    words = tokenize(query, False)
    if not words:
        return []

    kept = words[:-1]
    last = words[-1]

    def check_query(word):
        return bool(search_query(" ".join(kept + [word]), index))

    return [" ".join(kept + [word]) for word in trie.autocomplete(last, limit = limit, is_valid = check_query)]


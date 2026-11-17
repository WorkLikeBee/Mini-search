class TrieNode:
    __slots__ = ("children", "is_end_of_word")

    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

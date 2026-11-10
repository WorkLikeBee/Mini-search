from trie import Trie

def test_insert_mark_end_of_word():
    t = Trie()
    t.insert("data")
    assert (t.root.children["d"].children["a"].children["t"].children["a"].is_end_of_word == True)

def test_insert_prefix_is_not_a_word():
    t = Trie()
    t.insert("data")
    assert (t.root.children["d"].children["a"].children["t"].is_end_of_word == False)
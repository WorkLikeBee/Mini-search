from trie import Trie

def test_insert_mark_end_of_word():
    t = Trie()
    t.insert("data")
    assert (t.root.children["d"].children["a"].children["t"].children["a"].is_end_of_word == True)

def test_insert_prefix_is_not_a_word():
    t = Trie()
    t.insert("data")
    assert (t.root.children["d"].children["a"].children["t"].is_end_of_word == False)

def test_return_word_with_prefix():
    t = Trie()
    t.insert("data")
    t.insert("database")
    t.insert("dataset")
    t.insert("memory")
    assert (t.autocomplete("dat") == ["data", "database", "dataset"])

def test_auto_complete_including_itself():
    t = Trie()
    t.insert("data")
    t.insert("database")
    t.insert("dataset")
    t.insert("memory")
    assert (t.autocomplete("data") == ["data", "database", "dataset"])

def test_auto_complete_capital_case():
    t = Trie()
    t.insert("data")
    t.insert("database")
    t.insert("dataset")
    t.insert("memory")
    assert (t.autocomplete("DAT ") == ["data", "database", "dataset"])

def test_auto_complete_empty_prefix():
    t = Trie()
    t.insert("data")
    t.insert("database")
    t.insert("dataset")
    t.insert("memory")
    assert (t.autocomplete("") == ["data", "database", "dataset", "memory"])

def test_missing_prefix():
    t = Trie()
    t.insert("data")
    t.insert("database")
    t.insert("dataset")
    t.insert("memory")
    assert (t.autocomplete("xyz") == [])
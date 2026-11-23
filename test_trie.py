from trie import Trie, complete_query
from index import build_index, build_vocab

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

def test_auto_complete_with_cap_limit():
    t = Trie()
    for word in ["abe", "abd", "abc", "ab", "a"]:
        t.insert(word)

    assert (t.autocomplete("a", limit=3) == ["a","ab","abc"])

def test_auto_complete_reverse_with_cap_limit():
    t = Trie()
    for word in ["a", "ab", "abc", "abd", "abe"]:
        t.insert(word)

    assert (t.autocomplete("a", limit=3) == ["a", "ab", "abc"])


def test_missing_prefix():
    t = Trie()
    t.insert("data")
    t.insert("database")
    t.insert("dataset")
    t.insert("memory")
    assert (t.autocomplete("xyz") == [])

COMPLETE_DOCS = [
    {"id": 1, "title": "Software Engineering", "text": "design and testing"},
    {"id": 2, "title": "End Notes", "text": "summary"},
]

def make_index_and_trie():
    index = build_index(COMPLETE_DOCS)
    vocab = build_vocab(COMPLETE_DOCS)
    trie = Trie()
    for word in vocab:
        trie.insert(word)
    return index, trie

def test_complete_query_keeps_earlier_words():
    index, trie = make_index_and_trie()
    assert complete_query("software en", trie, index) == ["software engineering"]

def test_complete_query_one_word():
    index, trie = make_index_and_trie()
    assert complete_query("en", trie, index) == ["end", "engineering"]

def test_complete_query_empty():
    index, trie = make_index_and_trie()
    assert complete_query("", trie, index) == []

def test_complete_query_no_match():
    index, trie = make_index_and_trie()
    assert complete_query("software xyz", trie, index) == []

def test_complete_query_capitals_and_punctuation():
    index, trie = make_index_and_trie()
    assert complete_query("Software, En", trie, index) == complete_query("software en", trie, index)

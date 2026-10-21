from main import tokenize, build_index, search_query, intersect

def test_tokenize():
    text = "Hello World"
    result = tokenize(text)
    assert result == ["hello", "world"]

def test_tokenize_remove_punctuation():
    text = "Hello, World"
    result = tokenize(text)
    assert result == ["hello", "world"]

def test_tokenize_punctuation_only():
    text = "!!!"
    result = tokenize(text)
    assert result == []

def test_intersect_find_common_id():
    list_a = [1,3,5]
    list_b = [2,3,7]
    result = intersect(list_a, list_b)
    assert result == [3]

def test_tokenize_splits_hyphenated_word():
    text = "linked-list"
    result = tokenize(text)
    assert result == ["linked", "list"]

SAMPLE_DOCS = [
    {"id": 1, "title": "Doc One", "text": "data structures and algorithms"},
    {"id": 2, "title": "Doc Two", "text": "data and memory"},
    {"id": 3, "title": "Doc Three", "text": "memory management"},
]

def test_search_single_word():
    index = build_index(SAMPLE_DOCS)
    result = search_query("data", index)
    assert result == [1,2]





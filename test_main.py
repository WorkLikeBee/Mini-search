from main import tokenize, build_index, search_query, intersect, build_term_counts

def test_tokenize_lower_words():
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

def test_tokenize_splits_hyphenated_word():
    text = "linked-list"
    result = tokenize(text)
    assert result == ["linked", "list"]

def test_intersect_find_common_id():
    list_a = [1,3,5]
    list_b = [2,3,7]
    result = intersect(list_a, list_b)
    assert result == [3]

def test_intersect_no_common():
    list_a = [1]
    list_b = [2]
    result = intersect(list_a, list_b)
    assert result == []

def test_intersect_with_empty_list():
    list_a = []
    list_b = [3,5]
    result = intersect(list_a, list_b)
    assert result == []

SAMPLE_DOCS = [
    {"id": 1, "title": "Doc One", "text": "data structures and data algorithms"},
    {"id": 2, "title": "Doc Two", "text": "data and memory"},
    {"id": 3, "title": "Doc Three", "text": "memory management"},
]

def test_search_multiple_word():
    index = build_index(SAMPLE_DOCS)
    result = search_query("data memory", index)
    assert result == [2]

def test_search_missing_2nd_words():
    index = build_index(SAMPLE_DOCS)
    result = search_query("data zzz", index)
    assert result == []

def test_search_missing_word():
    index = build_index(SAMPLE_DOCS)
    result = search_query("dat ",index)
    assert result == []

def test_search_empty_query():
    index = build_index(SAMPLE_DOCS)
    result = search_query("",index)
    assert result == []

def test_search_single_word():
    index = build_index(SAMPLE_DOCS)
    result = search_query("data", index)
    assert result == [1,2]

def test_build_term_count():
    result = build_term_counts(SAMPLE_DOCS) 
    assert result == {
    1: {"data": 2, "structures": 1, "and": 1, "algorithms": 1},
    2: {"data": 1, "and": 1, "memory": 1},
    3: {"memory": 1, "management": 1},
}
from tokenizer import tokenize, use_stemming
from index import build_index, search_query, intersect, union, search_query_any
from ranking import build_term_counts, compute_idf, rank_results, build_doc_lengths
import math

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
    assert result == ["link", "list"]

def test_stemming_word():
    result = use_stemming("uses")
    assert result == "use"

def test_stem_strips_suffixes():
    assert use_stemming("sorting") == "sort"
    assert use_stemming("sorted") == "sort"
    assert use_stemming("sorts") == "sort"

def test_stem_es_only_after_s_x_z_ch_sh():
    assert use_stemming("classes") == "class"
    assert use_stemming("boxes") == "box"
    assert use_stemming("files") == "file"
    assert use_stemming("changes") == "change"

def test_stem_leaves_protected_words():
    for word in ["string", "thing", "class", "this", "status", "is"]:
        assert use_stemming(word) == word

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

def test_union_shared_id():
    list_a = [1,2,3]
    list_b = [3,4,5]
    result = union(list_a, list_b)
    assert result == [1,2,3,4,5]

def test_union_with_empty_list():
    result = union([], [1,2])
    assert result == [1,2]

def test_union_check_drop_out_last_item():
    list_a = [1,5]
    list_b = [2]
    result = union(list_a, list_b)
    assert result == [1,2,5]

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

def test_search_title_only():
    index = build_index(SAMPLE_DOCS)
    result = search_query("one", index)

    assert result == [1]

def test_search_any_with_one_missing():
    index = build_index(SAMPLE_DOCS)
    result = search_query_any("data zzz", index)

    assert result == [1,2]

def test_search_any():
    index = build_index(SAMPLE_DOCS)
    result = search_query_any("data management", index)

    assert result == [1,2,3]

def test_search_any_empty_query():
    index = build_index(SAMPLE_DOCS)
    result = search_query_any(" ", index)

    assert result == []

def test_search_any_not_found_query():
    index = build_index(SAMPLE_DOCS)
    result = search_query_any("zzz yyy", index)

    assert result == []

def test_search_matches_different_word_forms():
    docs = [
        {"id": 1, "title": "A", "text": "the list is sorted"},
        {"id": 2, "title": "B", "text": "nothing here"},
    ]
    index = build_index(docs)
    assert search_query("sorting", index) == [1]

def test_build_term_count():
    result = build_term_counts(SAMPLE_DOCS)
    assert result == {
    1: {"doc": 1, "one": 1,"data": 2, "structure": 1, "and": 1, "algorithm": 1},
    2: {"doc": 1, "two": 1,"data": 1, "and": 1, "memory": 1},
    3: {"doc": 1, "three": 1, "memory": 1, "management": 1},
}

def test_build_doc_lengths():
    term_counts = build_term_counts(SAMPLE_DOCS)
    result = build_doc_lengths(term_counts)

    assert result == {
        1: 7,
        2: 5,
        3: 4
    }

def test_compute_idf_with_word():
    index = build_index(SAMPLE_DOCS)
    df = len(index.get("management", []))
    n = len(SAMPLE_DOCS)
    result = compute_idf("management", index, n)
    assert result == math.log((n - df + 0.5) / (df + 0.5) + 1)

def test_compute_idf_no_word():
    index = build_index(SAMPLE_DOCS)
    df = len(index.get(" ", []))
    n = len(SAMPLE_DOCS)
    result = compute_idf(" ", index, n)
    assert result == math.log((n - df + 0.5) / (df + 0.5) + 1)

def test_rank_result_by_frequency():
    index = build_index(SAMPLE_DOCS)
    matches = search_query("data", index)
    total_docs = len(SAMPLE_DOCS)
    term_counts = build_term_counts(SAMPLE_DOCS)
    doc_lengths = build_doc_lengths(term_counts)
    avg_length = sum(doc_lengths.values()) / len(doc_lengths)

    result = rank_results(matches, "data", term_counts, index, total_docs, doc_lengths, avg_length)
    assert result == [1, 2]

def test_rank_results_higher_frequency_first():
    docs = [
        {"id": 1, "title": "A", "text": "memory"},
        {"id": 2, "title": "B", "text": "memory memory memory"},
        {"id": 3, "title": "C", "text": "networks"},
    ]
    index = build_index(docs)
    term_counts = build_term_counts(docs)
    matches = search_query("memory", index)
    doc_lengths = build_doc_lengths(term_counts)
    avg_length = sum(doc_lengths.values()) / len(doc_lengths)

    result = rank_results(matches, "memory", term_counts, index, len(docs), doc_lengths, avg_length)

    assert result == [2, 1]

def test_rank_results_tie_keeps_id_order():
    index = build_index(SAMPLE_DOCS)
    term_counts = build_term_counts(SAMPLE_DOCS)
    matches = search_query("memory", index)
    doc_lengths = build_doc_lengths(term_counts)
    avg_length = sum(doc_lengths.values()) / len(doc_lengths)

    result = rank_results(matches, "memory", term_counts, index, len(SAMPLE_DOCS), doc_lengths, avg_length)
    assert result == [3, 2]

def test_rank_results_empty_matches():
    index = build_index(SAMPLE_DOCS)
    term_counts = build_term_counts(SAMPLE_DOCS)
    doc_lengths = build_doc_lengths(term_counts)
    avg_length = sum(doc_lengths.values()) / len(doc_lengths)
    result = rank_results([], "memory", term_counts, index, len(SAMPLE_DOCS), doc_lengths, avg_length)

    assert result == []

def test_rank_result_matches_beat_frequency():
    index = build_index(SAMPLE_DOCS)
    term_counts = build_term_counts(SAMPLE_DOCS)
    matches = search_query_any("data memory", index)
    doc_lengths = build_doc_lengths(term_counts)
    avg_length = sum(doc_lengths.values()) / len(doc_lengths)

    result = rank_results(matches, "data memory", term_counts, index, len(SAMPLE_DOCS), doc_lengths, avg_length)
    assert result == [2,1,3]

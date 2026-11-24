from spelling import edit_distance, correct_query
from index import build_index, build_vocab


# ---------- edit_distance ----------

def test_edit_distance_identical_words():
    assert edit_distance("abc", "abc") == 0

def test_edit_distance_empty_strings():
    assert edit_distance("", "") == 0
    assert edit_distance("", "abc") == 3
    assert edit_distance("abc", "") == 3

def test_edit_distance_one_substitution():
    assert edit_distance("cat", "cut") == 1

def test_edit_distance_one_insert():
    assert edit_distance("cat", "cart") == 1

def test_edit_distance_one_delete():
    assert edit_distance("cart", "cat") == 1

def test_edit_distance_classic_example():
    # k→s, e→i, insert g
    assert edit_distance("kitten", "sitting") == 3

def test_edit_distance_different_lengths():
    # catches a table that is one row/column too small
    assert edit_distance("sunny", "supernatural") == 9

def test_edit_distance_is_symmetric():
    assert edit_distance("sunny", "supernatural") == edit_distance("supernatural", "sunny")

def test_edit_distance_swap_costs_two():
    # plain Levenshtein has no "swap" operation
    assert edit_distance("pyhton", "python") == 2


# ---------- correct_query ----------

def make_index_and_vocab(docs):
    return build_index(docs), build_vocab(docs)

def test_correct_query_fixes_one_word():
    docs = [{"id": 1, "title": "x", "text": "python"}]
    index, vocab = make_index_and_vocab(docs)
    assert correct_query("pyhton", vocab, index) == ["python"]

def test_correct_query_closest_word_first():
    docs = [{"id": 1, "title": "x", "text": "recursion revision"}]
    index, vocab = make_index_and_vocab(docs)
    # recursion is 1 edit away, revision is 2
    assert correct_query("recusion", vocab, index) == ["recursion", "revision"]

def test_correct_query_ties_are_alphabetical():
    docs = [{"id": 1, "title": "x", "text": "git gist"}]
    index, vocab = make_index_and_vocab(docs)
    assert correct_query("gitt", vocab, index) == ["gist", "git"]

def test_correct_query_short_word_allows_one_edit():
    docs = [{"id": 1, "title": "x", "text": "gt gui git anti"}]
    index, vocab = make_index_and_vocab(docs)
    # git and anti are 2 edits from gti, too far for a 3-letter word
    assert correct_query("gti", vocab, index) == ["gt", "gui"]

def test_correct_query_keeps_earlier_words():
    docs = [{"id": 1, "title": "x", "text": "javascript array"}]
    index, vocab = make_index_and_vocab(docs)
    assert correct_query("javascript arrray", vocab, index) == ["javascript array"]

def test_correct_query_skips_phrases_with_no_document():
    docs = [
        {"id": 1, "title": "x", "text": "git revision"},
        {"id": 2, "title": "y", "text": "recursion"},
    ]
    index, vocab = make_index_and_vocab(docs)
    # recursion is closer, but no document has both git and recursion
    assert correct_query("git recusion", vocab, index) == ["git revision"]

def test_correct_query_respects_limit():
    docs = [{"id": 1, "title": "x", "text": "cat cot cut"}]
    index, vocab = make_index_and_vocab(docs)
    assert correct_query("cbt", vocab, index, limit=2) == ["cat", "cot"]

def test_correct_query_no_close_word():
    docs = [{"id": 1, "title": "x", "text": "python"}]
    index, vocab = make_index_and_vocab(docs)
    assert correct_query("xqzv", vocab, index) == []

def test_correct_query_empty_query():
    docs = [{"id": 1, "title": "x", "text": "python"}]
    index, vocab = make_index_and_vocab(docs)
    assert correct_query("", vocab, index) == []

# Mini-search

A full-text search engine built from scratch in Python, with TF-IDF ranking and trie-based autocomplete.

## Background

I found it interesting that when we ask Google to search for something, it shows the best match first. I built this project to learn how that works.

## Demo

```
Enter query: dev*
Suggestions:  ['development']
Enter query: development
[9] Mobile App Development
[8] Web Development
[5] Software Engineering
Enter query: softw
Result not found
Enter query: soft*
Suggestions:  ['software']
Enter query: software
[5] Software Engineering
Enter query: software engineering
[5] Software Engineering
Enter query: q
```

Document 9 ranks first because it mentions "development" the most. A plain search like `softw` only matches whole words, while adding `*` asks for suggestions that start with that prefix.

A full-text search engine builds a word-to-ID map from the dataset. It then uses the user's input to find the matching document(s) through the index, and ranks the results using the TF-IDF method. If the user is unsure of the spelling, they can type `*` at the end, and the engine will suggest words that start with what they typed.

## Features

- Multi-word search
- Ranked results using TF-IDF
- Prefix autocomplete
- Case-insensitive search and punctuation handling

## How it works

```
query → tokenize → inverted index lookup → intersect → rank (TF-IDF) → results
```

1. **Tokenize:** turn the query into tokens (a list of words)
2. **Inverted index:** build a word-to-ID map
3. **Intersect:** find the results that match all the tokens
4. **Rank:** rank the results using the TF-IDF method

**Autocomplete:** the trie is a data structure built from nodes. Each node has a map of its children and a boolean that marks whether the path to it spells a complete word. A node can be the end of a word and still have children: "data" is a complete word, but it continues into "database" and "dataset." The trie has two main functions: insert a word, and autocomplete a prefix to give suggestions.
The autocomplete function walks down the path that matches the prefix, then explores every path below it, collects each complete word it finds, and returns the suggestions in a list.

## Design decisions

**Duplicate prevention in O(1).** Documents are indexed in increasing ID order, so if a word's posting list already contains the current document, it must be the last entry. Checking only the last element avoids an O(n) membership scan.

**Two-pointer intersection.** Each word's list of document IDs is already sorted, because documents are indexed in ID order. Two pointers walk both lists at once, always advancing the pointer at the smaller ID, and record a match when the IDs are equal. This runs in O(n + m) time, where n and m are the lengths of the two lists, and needs no extra data structures like sets.

**Filtering separate from ranking.** `search_query` finds which documents contain every query word, and `rank_results` orders them by relevance. Keeping these as separate steps means each one can be tested and changed on its own. Adding ranking didn't require touching the search code or its tests.

**Term counts in a separate structure.** TF-IDF needs to know how many times each word appears in each document, but the inverted index only stores which documents contain a word. Instead of changing the index (which would have broken the intersection code), word counts live in their own dictionary: document ID → word → count.

**Punctuation becomes a space.** Replacing punctuation with a space splits `linked-lists` into `linked` and `lists`, so either word finds the document. The tradeoff is that `don't` becomes `don` and `t`. Hyphenated terms are more common in technical text, so splitting was the better choice here.

**Trie for autocomplete.** Words that share a prefix share a path in the trie. Finding suggestions takes O(P + K) time, where P is the prefix length and K is the number of nodes below it, instead of checking every word in the vocabulary. The trie is built from the inverted index's keys, so suggestions always match words that can actually be searched.

## Getting started

```bash
git clone https://github.com/WorkLikeBee/Mini-search.git
cd Mini-search
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python main.py
```

- Type a query to search, e.g. `development`
- End a query with `*` for suggestions, e.g. `dev*`
- Type `q` to quit

Run the tests:

```bash
python -m pytest -v
```

## Project structure

```
main.py                 # Loads data, builds the index, ranking data, and trie; runs the search loop
tokenizer.py            # Lowercases text, removes punctuation, splits into words
index.py                # Builds the inverted index; multi-word search with two-pointer intersection
ranking.py              # Term counts, IDF, and TF-IDF ranking
trie.py                 # Trie with insert and prefix autocomplete
trie_node.py            # A single trie node (children and end-of-word marker)
data.json               # Sample documents
test_search_engine.py   # Tests for tokenizer, search, and ranking
test_trie.py            # Tests for the trie and autocomplete
```

## Roadmap

- [X] Make document titles searchable (currently only the text is indexed)
- [ ] Autocomplete the last word of a multi-word query, e.g. `software eng*`
- [ ] OR-style search, so documents matching most (not all) query words still appear, ranked lower
- [ ] Real data from an API such as Hacker News or Wikipedia
- [ ] Web API and search page
- [ ] Rewrite the index core in C and benchmark it against Python
# Mini-search

Full-text search engine built from scratch with Python

## Background

I found it interesting how we can ask Google to search for something and they will give the best match option on top.

## Demo

```
Enter query: dev*
Suggestions:  ['development']
Enter query: development
[9] Mobile App Development
[5] Software Engineering
[8] Web Development
Enter query: softw
Result not found
Enter query: soft*
Suggestions:  ['software']
Enter query: q
```

A full-text search engine will build an word-to-id map based on the dataset. Then it will use the input from the user to search the expected document(s) through the index, and then rank the result using TF-IDF method. If the user is unsure about the word-spell, the user can type "*" at the end so that the engine will provide suggestions if found.

## Features

- Multi-word search
- Ranking result using TF-IDF method
- Prefix autocomplete
- case-insensitive searching and punctuation handling

## How it works

```
query → tokenize → inverted index lookup → intersect → rank (TF-IDF) → results
```

1. **Tokenize:** turn the query into tokens (a list of words)
2. **Inverted index:** build word-to-id map
3. **Intersect:** find the results that match all the tokens
4. **Rank:** ranking the results using TF - IDF method

Autocomplete: the trie is a data structure built from nodes. Each node will have a children map essentially, and a boolean value to determine whether it is the end of the branch. The trie will have some basic functions to insert branches and autocomplete using prefix to give instruction.
The autocomplete function will look for the branches that have the prefix and then walk till the end of those branches, then return the suggested words in a list. 

Design decisions
<!-- What you chose, why, and the time complexity where you can. -->

Duplicate prevention in O(1). Documents are indexed in increasing ID order, so if a word's posting list already contains the current document, it must be the last entry. Checking only the last element avoids an O(n) membership scan.

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

Roadmap
 TODO: web API and search page
 TODO: real data (e.g. Hacker News or Wikipedia)
 TODO: rewrite the index core in C and benchmark it
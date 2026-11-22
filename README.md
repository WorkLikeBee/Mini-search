# Mini-search

A full-text search engine built from scratch in Python, with BM25 ranking and trie-based autocomplete, searching about 900 of the most-voted Stack Overflow questions.

## Background

I found it interesting that when we ask Google to search for something, it shows the best match first. I built this project to learn how that works.

## Demo

```
Enter query: py*
Suggestions:  ['py', 'py2', 'pyenv', 'pypi', 'python', 'pythonic', 'pythonicest', 'pythonista', 'pyvenv']
Enter query: python
[762] What is the Python 3 equivalent of "python -m SimpleHTTPServer"  |  https://stackoverflow.com/questions/7943751/what-is-the-python-3-equivalent-of-python-m-simplehttpserver
[857] Null object in Python  |  https://stackoverflow.com/questions/3289601/null-object-in-python
[21] Does Python have a ternary conditional operator?  |  https://stackoverflow.com/questions/394809/does-python-have-a-ternary-conditional-operator
[709] Replacements for switch statement in Python?  |  https://stackoverflow.com/questions/60208/replacements-for-switch-statement-in-python
[125] How do I get the current time in Python?  |  https://stackoverflow.com/questions/415511/how-do-i-get-the-current-time-in-python
[830] How do I move a file in Python?  |  https://stackoverflow.com/questions/8858008/how-do-i-move-a-file-in-python
[210] How do I concatenate two lists in Python?  |  https://stackoverflow.com/questions/1720421/how-do-i-concatenate-two-lists-in-python
[166] How can I delete a file or folder in Python?  |  https://stackoverflow.com/questions/6996603/how-can-i-delete-a-file-or-folder-in-python
[177] How can I access environment variables in Python?  |  https://stackoverflow.com/questions/4906977/how-can-i-access-environment-variables-in-python
[614] Use a different Python version with virtualenv  |  https://stackoverflow.com/questions/1534210/use-a-different-python-version-with-virtualenv
Enter query: software*
Suggestions:  ['software']
Enter query: software
[799] Cycles in family tree software  |  https://stackoverflow.com/questions/6163683/cycles-in-family-tree-software
[481] What is move semantics?  |  https://stackoverflow.com/questions/3106110/what-is-move-semantics
[524] What is the difference between a process and a thread?  |  https://stackoverflow.com/questions/200469/what-is-the-difference-between-a-process-and-a-thread
[87] How is Docker different from a virtual machine?  |  https://stackoverflow.com/questions/16047306/how-is-docker-different-from-a-virtual-machine
Enter query: hide in b*
Suggestions:  No suggestions
Enter query: git commit r*
Suggestions:  No suggestions
Enter query: git commit
[175] What does cherry-picking a commit with Git mean?  |  https://stackoverflow.com/questions/9339429/what-does-cherry-picking-a-commit-with-git-mean
[528] How to undo "git commit --amend" done instead of "git commit"  |  https://stackoverflow.com/questions/1459150/how-to-undo-git-commit-amend-done-instead-of-git-commit
[9] How do I undo 'git add' before commit?  |  https://stackoverflow.com/questions/348170/how-do-i-undo-git-add-before-commit
[804] Remove a git commit which has not been pushed  |  https://stackoverflow.com/questions/1611215/remove-a-git-commit-which-has-not-been-pushed
[272] How do I get the hash for the current commit in Git?  |  https://stackoverflow.com/questions/949314/how-do-i-get-the-hash-for-the-current-commit-in-git
[29] How do I revert a Git repository to a previous commit?  |  https://stackoverflow.com/questions/4114095/how-do-i-revert-a-git-repository-to-a-previous-commit
[664] How can I generate a Git patch for a specific commit?  |  https://stackoverflow.com/questions/6658313/how-can-i-generate-a-git-patch-for-a-specific-commit
[186] How do I modify a specific commit?  |  https://stackoverflow.com/questions/1186535/how-do-i-modify-a-specific-commit
[169] How do I make git use the editor of my choice for editing commit messages?  |  https://stackoverflow.com/questions/2596805/how-do-i-make-git-use-the-editor-of-my-choice-for-editing-commit-messages
[147] Commit only part of a file's changes in Git  |  https://stackoverflow.com/questions/1085162/commit-only-part-of-a-files-changes-in-git
Enter query: q

```

Typing `*` at the end of a query asks for suggestions, drawn from the real vocabulary of the questions. A normal query returns the 10 most relevant questions, each with a link to the original on Stack Overflow.

A full-text search engine builds a word-to-ID map from the dataset. It then uses the user's input to find the matching document(s) through the index, and ranks the results using the BM25 method. If the user is unsure of the spelling, they can type `*` at the end, and the engine will suggest words that start with what they typed.

## Features

- Searches real Stack Overflow questions, fetched from the Stack Exchange API
- Multi-word search: documents matching any query word are returned, with full matches ranked first
- Ranked results using BM25, showing the top 10 with links
- Prefix autocomplete, including the last word of a multi-word query
- Searches both question titles and text
- Case-insensitive search and punctuation handling

## How it works

**Getting the data** (`fetch_data.py`):

```
Stack Exchange API → page through results → skip duplicates and closed questions → clean HTML → number documents → save JSON
```

**Searching** (`main.py`):

```
query → tokenize → inverted index lookup → union → rank (matched words, then BM25) → top 10 results
```

1. **Tokenize:** turn the query into tokens (a list of words)
2. **Inverted index:** build a word-to-ID map covering each document's title and text
3. **Combine:** find every document that contains at least one query word
4. **Rank:** sort by how many distinct query words each document contains, then by BM25 score, and show the top 10

**Autocomplete:** the trie is a data structure built from nodes. Each node has a map of its children and a boolean that marks whether the path to it spells a complete word. A node can be the end of a word and still have children: "data" is a complete word, but it continues into "database" and "dataset." The trie has two main functions: insert a word, and autocomplete a prefix to give suggestions.
The autocomplete function walks down the path that matches the prefix, then explores every path below it in alphabetical order, collects each complete word it finds (up to a limit), and returns the suggestions in a list. For a multi-word query, only the last word is completed, and a suggestion is kept only if all of its words appear together in at least one document.

## Design decisions

### Search engine

**Duplicate prevention in O(1).** Documents are indexed in increasing ID order, so if a word's posting list already contains the current document, it must be the last entry. Checking only the last element avoids an O(n) membership scan.

**Two-pointer intersection and union.** Each word's list of document IDs is already sorted, because documents are indexed in ID order. Two pointers walk both lists at once, always advancing the pointer at the smaller ID. Intersection keeps only IDs found in both lists; union (the merge step from merge sort) keeps every ID once. Both run in O(n + m) time, where n and m are the lengths of the two lists, and need no extra data structures like sets.

**Ranked by matched words, then BM25.** Search returns documents containing any query word. Results are sorted by a two-part key: the number of distinct query words a document contains, then its BM25 score. A document matching the whole query always beats one that repeats a single word many times, and BM25 breaks ties.

**BM25 instead of plain TF-IDF.** Plain TF-IDF rewards a word every time it repeats, so long questions that mention a word often outrank short, focused ones. BM25 fixes this in two ways: term frequency saturates (the tenth repeat adds far less than the second), and each document's score is normalized by its length relative to the average (`k1 = 1.5`, `b = 0.75`). Document lengths are computed once from the term counts, so ranking needs no extra pass over the text. The matched-words count stays the first sort key, so BM25 only orders documents that match the same number of query words.

**Rank first, then trim.** All matching documents are ranked before the top 10 are taken. An earlier version trimmed to 10 before ranking, which kept the 10 lowest IDs instead of the 10 best matches.

**Filtering separate from ranking.** `search_query_any` finds candidate documents, and `rank_results` orders them by relevance. Keeping these as separate steps means each one can be tested and changed on its own.

**Term counts in a separate structure.** BM25 needs to know how many times each word appears in each document, but the inverted index only stores which documents contain a word. Instead of changing the index (which would have broken the intersection code), word counts live in their own dictionary: document ID → word → count.

**One shared source of searchable text.** A single `searchable_text` helper combines a document's title and text, and both the index and the term counts use it, so search and ranking can never see different words.

**Punctuation becomes a space.** Replacing punctuation with a space splits `linked-lists` into `linked` and `lists`, so either word finds the document. The tradeoff is that `don't` becomes `don` and `t`. Hyphenated terms are more common in technical text, so splitting was the better choice here.

**Trie for autocomplete.** Words that share a prefix share a path in the trie. Finding suggestions takes O(P + K) time, where P is the prefix length and K is the number of nodes below it, instead of checking every word in the vocabulary. The trie is built from the inverted index's keys, so suggestions always match words that can actually be searched.

**Autocomplete limit with early stopping.** Children are visited in sorted order, so the depth-first search finds words alphabetically. Once the limit is reached, the search stops instead of walking the rest of the trie, which keeps short prefixes fast on a large vocabulary.

**Suggestions are stricter than search.** Search uses OR so it always tries to return something useful, but multi-word suggestions use AND: a suggestion is only shown if all of its words appear together in at least one document, so it never leads to a phrase that finds nothing.

### Data pipeline

**Documents are numbered locally.** Stack Overflow question IDs arrive in vote order, not numeric order, but the index relies on increasing IDs. Each document gets its own sequential ID (1, 2, 3...), and the original question ID and link are kept as separate fields.

**Code blocks are removed before indexing.** Multi-line code blocks are full of variable names like `i` and `x`, so they're stripped out and searches match the question's explanation instead. Inline code, like function names in a sentence, is kept.

**Tags are stripped before entities are decoded.** Decoding first would turn `&lt;algorithm&gt;` into `<algorithm>`, which the tag-stripping step would then delete as if it were HTML.

**Well-behaved API client.** The fetcher stops on API errors instead of retrying blindly, waits when the API sends a `backoff` value, stops when there are no more pages, and uses a request timeout.

**Duplicates skipped across pages.** Vote counts can change while paging, so a question can move from one page to the next and appear twice. A set of seen question IDs skips repeats in O(1) per question.

## Getting started

```bash
git clone https://github.com/WorkLikeBee/Mini-search.git
cd Mini-search
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python fetch_data.py             # downloads ~900 questions (uses 10 of the API's 300 free daily requests)
python main.py
```

- Type a query to search, e.g. `python`
- End a query with `*` for suggestions, e.g. `py*`
- Type `q` to quit

Run the tests:

```bash
python -m pytest -v
```

## Project structure

```
main.py                 # Loads data, builds the index, ranking data, and trie; runs the search loop
fetch_data.py           # Fetches questions from the Stack Exchange API, cleans them, and saves them as JSON
tokenizer.py            # Lowercases text, removes punctuation, splits into words; combines title and text
index.py                # Builds the inverted index; AND and OR search with two-pointer intersection and union
ranking.py              # Term counts, document lengths, IDF, and ranking by matched words then BM25
trie.py                 # Trie with insert, limited prefix autocomplete, and multi-word query completion
trie_node.py            # A single trie node (children and end-of-word marker)
test_search_engine.py   # Tests for tokenizer, search, and ranking
test_trie.py            # Tests for the trie and autocomplete
data_stackoverflow.json # Generated by fetch_data.py (not committed)
```

## Roadmap

- [x] Make document titles searchable
- [x] Autocomplete the last word of a multi-word query, e.g. `software eng*`
- [x] Cap autocomplete results, stopping the search early once enough words are found
- [x] OR-style search, so documents matching most (not all) query words still appear, ranked lower
- [x] Real data from the Stack Exchange API

Problems found by testing on real data:

- [x] Length normalization (BM25), so long questions don't rank higher just for mentioning more words
- [ ] Stemming, so `sort`, `sorted`, and `sorting` match each other
- [ ] Stop words or IDF-weighted match counts, so common words like "in" don't count as much as rare ones
- [ ] Filter autocomplete candidates before applying the limit, so valid multi-word suggestions aren't cut off
- [ ] Spelling correction with edit distance, so typos like `ciber*` still find suggestions

Bigger next steps:

- [ ] Web API and search page
- [ ] Rewrite the index core in C and benchmark it against Python

## Data attribution

Question data comes from [Stack Overflow](https://stackoverflow.com) via the Stack Exchange API and is licensed under [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/). Every search result links to the original question.

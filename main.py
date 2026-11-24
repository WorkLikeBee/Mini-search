import json
from index import build_index, search_query_any, build_vocab
from ranking import build_term_counts, rank_results, build_doc_lengths
from trie import Trie, complete_query
from spelling import correct_query


def load_document(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    try:
        documents = load_document("data_stackoverflow.json")
    except FileNotFoundError:
        print("data_stackoverflow.json not found. Run `python fetch_data.py` first to download questions (uses 10 API requests).")
        return

    index = build_index(documents)
    vocabs = build_vocab(documents)
    term_counts = build_term_counts(documents)
    docs_length = build_doc_lengths(term_counts)
    average_docs_length = sum(docs_length.values()) / len(docs_length)
    id_to_doc = {doc["id"]: (doc["title"], doc.get("link")) for doc in documents}
    total_docs = len(documents)

    trie = Trie()
    for token in vocabs:
        trie.insert(token)

    while True:
        query = input("Enter query: ").strip()
        if query.lower() == "q":
            break

        if query.endswith("*"):
            suggestions = complete_query(query[:-1], trie, index)
            if suggestions:
                print("Suggestions: ", suggestions)
            else:
                corrections = correct_query(query[:-1], vocabs, index)
                print("Did you mean: ", corrections if corrections else "No suggestions")
            continue

        matches = search_query_any(query, index)
        results = rank_results(matches, query, term_counts, index, total_docs, docs_length, average_docs_length)
        if not results:
            print("Result not found")
            continue

        for doc_id in results[:10]:
            print(f"[{doc_id}] {id_to_doc[doc_id][0]}  |  {id_to_doc[doc_id][1]} ")


if __name__ == "__main__":
    main()

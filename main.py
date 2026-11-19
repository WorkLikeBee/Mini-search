import json
from index import build_index, search_query_any
from ranking import build_term_counts, rank_results
from trie import Trie, complete_query


def load_document(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def main():
    documents = load_document("data_stackoverflow.json")
    index = build_index(documents)
    term_counts = build_term_counts(documents)
    id_to_doc = {doc["id"]: (doc["title"], doc.get("link")) for doc in documents}
    total_docs = len(documents)

    trie = Trie()
    for token in index:
        trie.insert(token)

    while True:
        query = input("Enter query: ").strip()
        if query.lower() == "q":
            break

        if query.endswith("*"):
            suggestions = complete_query(query[:-1], trie, index)
            print("Suggestions: ", suggestions if suggestions else "No suggestions")
            continue

        matches = search_query_any(query, index)
        results = rank_results(matches, query, term_counts, index, total_docs)
        if not results:
            print("Result not found")
            continue

        for doc_id in results[:10]:
            print(f"[{doc_id}] {id_to_doc[doc_id][0]}  |  {id_to_doc[doc_id][1]} ")


if __name__ == "__main__":
    main()

import json
from index import build_index, search_query
from ranking import build_term_counts, rank_results
from trie import Trie

def load_document(path):
    with open(path, "r", encoding="utf-8") as file:
        data_set = json.load(file)
        return data_set

if __name__ == "__main__":
    data_set = load_document("./data.json")
    index = build_index(data_set)
    term_counts = build_term_counts(data_set)
    id_to_title = {}
    total_docs = len(data_set)

    trie = Trie()
    for token in index:
        trie.insert(token)
    
    for data in data_set:
        id_to_title[data["id"]] = data["title"]

    while True: 
        word_search = input("Enter query: ").strip()
        if word_search.lower() == "q":
            break

        if (word_search.endswith("*")):
            word_search = word_search[:-1]
            suggestions = trie.autocomplete(word_search)
            if (not suggestions):
                print("No suggestions")
            else:
                print("Suggestions: ", suggestions)
        
        else:
            result = search_query(word_search, index)
            result = rank_results(result, word_search, term_counts, index, total_docs)
            if not result:
                print("Result not found")

            else:
                for doc_id in result:
                    print(f"[{doc_id}] {id_to_title[doc_id]}")

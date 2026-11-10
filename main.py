import json
from index import build_index, search_query
from ranking import build_term_counts, rank_results

def load_document(path):
    with open (path, "r") as file:
        data_set = json.load(file)
        return data_set


if __name__ == "__main__":
    data_set = load_document("./data.json")
    index = build_index(data_set)
    term_counts = build_term_counts(data_set)
    id_to_title = {}
    total_docs = len(data_set)
    for data in data_set:
        id_to_title[data["id"]] = data["title"]

    # print(index)
    # word_search = "software! and* "

    # print(search_query(word_search, index))
    while True: 
        word_search = input("Enter query: ")
        if word_search.strip().lower() == "q":
            break

        result = search_query(word_search, index)
        result = rank_results(result, word_search, term_counts, index, total_docs)
        if not result:
            print("Result not found")

        else:
            for doc_id in result:
                print(f"[{doc_id}] {id_to_title[doc_id]}")







import math
from tokenizer import tokenize,searchable_text

def compute_idf(word, index, total_docs):
    df = len(index.get(word, []))
    n = total_docs
    if df == 0:
        return 0

    return math.log(n/df)

def rank_results(matches, query, term_counts, index, total_docs):
    tokens = tokenize(query)
    ranking_keys = {}
    idf = {}

    for word in tokens:
        idf[word] = compute_idf(word, index, total_docs)

    for doc_id in matches:
        score = 0
        match_counts = 0
        for word in set(tokens):
            score += term_counts[doc_id].get(word, 0) * idf[word]
            if word in term_counts[doc_id]:
                match_counts += 1

        ranking_keys[doc_id] = (match_counts, score)

    return sorted(matches, key=lambda doc_id: ranking_keys[doc_id], reverse=True)

def build_term_counts(documents):
    id_to_counts = {}
    for document in documents:
        counts_dic = {}
        id_to_counts[document["id"]] = counts_dic
        tokens = tokenize(searchable_text(document))
        for token in tokens:
            if token not in counts_dic:
                counts_dic[token] = 1
            else:
                counts_dic[token] += 1

    return id_to_counts

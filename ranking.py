import math
from tokenizer import tokenize

def compute_idf(word, index, total_docs):
    df = len(index.get(word, []))
    n = total_docs
    if df == 0:
        return 0

    return math.log(n/df)

def rank_results(matches, query, term_counts, index, total_docs):
    tokens = tokenize(query)
    scores = {}
    idf = {}

    for word in tokens:
        idf[word] = compute_idf(word, index, total_docs)

    for doc_id in matches:
        score = 0 
        for word in tokens:
            score += term_counts[doc_id][word] * idf[word]

        scores[doc_id] = score

    return sorted(matches, key=lambda doc_id: scores[doc_id], reverse=True)

def build_term_counts(documents):
    id_to_counts = {}
    for doc in documents:
        counts_dic = {}
        id_to_counts[doc["id"]] = counts_dic
        tokens = tokenize(doc["text"])
        for token in tokens:
            if token not in counts_dic:
                counts_dic[token] = 1
            else:
                counts_dic[token] += 1

    return id_to_counts
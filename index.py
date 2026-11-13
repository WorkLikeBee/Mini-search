# return a dict mapping each word to a list of Ids:
from tokenizer import tokenize, searchable_text

def build_index(documents):
    index = {}
    for document in documents:
        tokens = tokenize(searchable_text(document))
        for token in tokens:
            if token not in index:
                index[token] = []
                index[token].append(document["id"])

            if index[token][-1] != document["id"]: index[token].append(document["id"])

    return index

def search_query(query, index):
    tokens = tokenize(query)
    if len(tokens) == 0: 
        return []

    result = index.get(tokens[0], [])

    for token in tokens[1:]:
        result = intersect(result, index.get(token, []))
        if not result:
            return result

    return result


def intersect(list_a, list_b):
    i = 0
    j = 0
    match_list = []
    while i < len(list_a) and j < len(list_b):
        if list_a[i] < list_b[j]:
            i+=1
        elif list_a[i] > list_b[j]:
            j+=1
        else:
            match_list.append(list_a[i])
            i += 1
            j += 1

    return match_list
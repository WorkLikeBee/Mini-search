from tokenizer import tokenize, searchable_text

def build_index(documents):
    """Map each word to a sorted list of the IDs of documents containing it."""
    index = {}
    for document in documents:
        doc_id = document["id"]
        for token in tokenize(searchable_text(document)):
            postings = index.setdefault(token, [])
            # Documents arrive in increasing ID order, so a duplicate can only be last.
            if not postings or postings[-1] != doc_id:
                postings.append(doc_id)

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
            i += 1
        elif list_a[i] > list_b[j]:
            j += 1
        else:
            match_list.append(list_a[i])
            i += 1
            j += 1

    return match_list

def union(list_a, list_b):
    i = 0
    j = 0
    merged = []
    while i < len(list_a) and j < len(list_b):
        if list_a[i] < list_b[j]:
            merged.append(list_a[i])
            i += 1
        elif list_a[i] > list_b[j]:
            merged.append(list_b[j])
            j += 1
        else:
            merged.append(list_a[i])
            i += 1
            j += 1

    for item in list_a[i:]:
        merged.append(item)

    for item in list_b[j:]:
        merged.append(item)

    return merged

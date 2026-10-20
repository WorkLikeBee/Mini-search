import json
import string

def load_document(path):
    with open (path, "r") as file:
        data_set = json.load(file)
        return data_set

def tokenize(text):
    #Reduce punctuation
    for char in string.punctuation:
        if char in text:
            text = text.replace(char, " ")

    return text.lower().split()


# print(tokenize("Data Structures: arrays, linked-lists & C."))

# return a dict mapping each word to a list of Ids:
def build_index(documents):
    index = {}
    for document in documents:
        tokens = tokenize(document["text"])
        for token in tokens:
            if token not in index:
                index[token] = []
                index[token].append(document["id"])

            if index[token][-1] != document["id"]: index[token].append(document["id"])

    return index

def search_query(query, index):
    token_searching = tokenize(query)[0]
    return index.get(token_searching, [])


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


data_set = load_document("./data.json")
index = build_index(data_set)
# print(index)
word_search = "development"

print(word_search + " ->", search_query(word_search, index))




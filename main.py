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


data_set = load_document("./data.json")
index = build_index(data_set)
print(index)




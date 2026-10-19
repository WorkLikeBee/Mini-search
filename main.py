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


text = tokenize("Data Structures: arrays, linked-lists & C.")

print(text)
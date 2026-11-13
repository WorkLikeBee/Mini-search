import string

def tokenize(text):
    #Reduce punctuation
    for char in string.punctuation:
        if char in text:
            text = text.replace(char, " ")

    return text.lower().split()

def searchable_text(document):
    return (document["title"] + " " + document["text"])
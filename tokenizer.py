import string

VOWELS = "aeiou"

def tokenize(text):
    #Reduce punctuation
    for char in string.punctuation:
        if char in text:
            text = text.replace(char, " ")

    return text.lower().split()

def stem(word):
    if len(word) <= 3:
        return word

    if word.endswith("ing"):
        remainder = word[:-3]
        if len(remainder) >= 3 and has_vowel(remainder):
            return remainder

    if word.endswith("ed"):
        remainder = word[:-2]
        if len(remainder) >= 3 and has_vowel(remainder):
            return remainder

    if word.endswith("es"):
        remainder = word[:-2]
        if remainder.endswith(("s", "x", "z", "ch", "sh")) and len(remainder) >= 3 and has_vowel(remainder):
            return remainder

    if word.endswith("s"):
        if not word.endswith(("ss", "us", "is")):
            remainder = word[:-1]
            if len(remainder) >= 3 and has_vowel(remainder):
                return remainder

    return word

def searchable_text(document):
    return (document["title"] + " " + document["text"])

def has_vowel(text):
    for char in text.lower():
        if char in VOWELS:
            return True

    return False

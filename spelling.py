from tokenizer import tokenize
from index import search_query

def correct_query(query, vocab, index, limit=10):
    """Suggest close spellings of the last word, keeping the earlier words."""
    tokens = tokenize(query, False)
    distance_to_word = []

    if not tokens:
        return []

    kept = tokens[:-1]
    last = tokens[-1]

    max_distance = 1 if len(last) <= 4 else 2
    for word in vocab:
        distance = edit_distance(last, word)
        if distance <= max_distance:
            distance_to_word.append((distance, word))

    def check_query(phrase):
        return bool(search_query(phrase, index))

    results = []
    for distance, word in sorted(distance_to_word):
        phrase = " ".join(kept + [word])
        if check_query(phrase):
            results.append(phrase)
            if len(results) == limit:
                break

    return results

def edit_distance(a, b):
    length_a = len(a)
    length_b = len(b)
    dp = [[0] * (length_a + 1) for _ in range(length_b + 1)]

    for j in range(len(dp[0])):
        dp[0][j] = j

    for i in range(len(dp)):
        dp[i][0] = i

    for i in range(1, length_b+1):
        for j in range (1, length_a+1):
            diagonal = dp[i-1][j-1]
            above = dp[i-1][j]
            left = dp[i][j-1]
            if a[j-1] == b[i-1]:
                dp[i][j] = diagonal
            else:
                dp[i][j] = (1 + min(diagonal, above, left))

    return dp[-1][-1]

import re

def word_map(text: str, separator, morse=True) -> dict:
    """Retrieve a word from a given index and separator."""
    words = [item.strip() for item in re.split(f'({re.escape(separator)})', text) if item]

    word_map = {}
    prev = 0
    for j, i in enumerate(words):
        c = prev + len(i.split() if morse else i)
        word_map[j + 1] = (prev+1, c)
        prev = c
    return word_map, words
    

def levenshtein_with_operations(sA, sB):
    """Compute Levenshtein distance with operations between Morse codes."""
    s1, s2 = sA.split(' '), sB.split(' ')
    len_s1, len_s2 = len(s1), len(s2)
    dp = [[0] * (len_s2 + 1) for _ in range(len_s1 + 1)]

    for i in range(len_s1 + 1):
        for j in range(len_s2 + 1):
            if i == 0:
                dp[i][j] = j
            elif j == 0:
                dp[i][j] = i
            elif s1[i - 1] == s2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],        # deletion
                                  dp[i][j - 1],        # insertion
                                  dp[i - 1][j - 1])    # substitution

    # Backtrack to find edit operations
    i, j = len_s1, len_s2
    operations = {}
    # morse_list = word_map(sA, '/')
    # word_list = word_map(word, ' ')
    while i > 0 or j > 0:
        if i > 0 and dp[i][j] == 1 + dp[i - 1][j]:
            operations[i] = f"You Forgot \"{s1[i - 1]}\""
            i -= 1
        elif j > 0 and dp[i][j] == 1 + dp[i][j - 1]:
            operations[i] = f"You added an extra \"{s2[j-1]}\""
            j -= 1
        else:
            if s1[i - 1] != s2[j - 1]:
                operations[i] = f"You wrote \"{s2[j-1]}\" instead of \"{s1[i-1]}\""
            i -= 1
            j -= 1

    return dp[len_s1][len_s2], operations
    
    
def display_errors(word_positions, errors, correct_sentence):
    # The correct sentence corresponding to the word positions
    words = correct_sentence.split(' / ')  # Assume sentence is split by " / " as a delimiter

    # Map positions to words for easier error grouping
    word_errors = {}
    for pos, error in errors.items():
        for word_index, (start_pos, end_pos) in word_positions.items():
            if start_pos <= pos <= end_pos:
                if word_index not in word_errors:
                    word_errors[word_index] = []
                word_errors[word_index].append(error)
                break

    # Output errors grouped by words
    for word_index, word in enumerate(words, 1):
        if word_index in word_errors:
            print(f"In the word '{word}' written as '{correct_sentence[word_positions[word_index][0] - 1:word_positions[word_index][1]]}':")
            for error in word_errors[word_index]:
                print(f"• {error}")



# for word_idx, (start, end) in word_map.items():
#     if start <= index <= end:
#         return words[word_idx]
# return None

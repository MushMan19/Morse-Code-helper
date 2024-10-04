import winsound
from colorama import Fore, Back, Style
import time
import re
import sys

# Constants
MORSE_FREQ = 500
DOT_DURATION = 100  # milliseconds

morse_alphabet = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----."
}


def text_to_morse(text: str, morse_dict=morse_alphabet) -> str:
    """Convert plain text to Morse code."""
    return ' '.join(morse_dict.get(char.upper(), char) if char != ' ' else '/' for char in text)


def morse_to_sound(morse_code: str, duration: int = DOT_DURATION, frequency: int = MORSE_FREQ) -> None:
    """Play sound for Morse code using beeps."""
    for symbol in morse_code:
        if symbol == ".":
            winsound.Beep(frequency, duration)
        elif symbol == "-":
            winsound.Beep(frequency, duration * 3)
        elif symbol == " ":
            time.sleep(duration * 3 / 1000)
        elif symbol == "/":
            time.sleep(duration / 1000)


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
                dp[i][j] = 1 + min(dp[i - 1][j],       # deletion
                                  dp[i][j - 1],        # insertion
                                  dp[i - 1][j - 1])    # substitution

    # Backtrack to find edit operations
    i, j = len_s1, len_s2
    operations = {}
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


def print_ct(text: str, color: str = 'white', background: str = None, style: str = 'normal', end: str = '\n') -> None:
    """Print text in color with optional background and style."""
    color_map = {
        'black': Fore.BLACK, 'red': Fore.RED, 'green': Fore.GREEN,
        'yellow': Fore.YELLOW, 'blue': Fore.LIGHTBLUE_EX, 'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN, 'white': Fore.WHITE
    }
    
    background_map = {
        'black': Back.BLACK, 'red': Back.RED, 'green': Back.GREEN,
        'yellow': Back.YELLOW, 'blue': Back.BLUE, 'magenta': Back.MAGENTA,
        'cyan': Back.CYAN, 'white': Back.WHITE
    }
    
    style_map = {'normal': Style.RESET_ALL, 'bold': Style.BRIGHT, 'dim': Style.DIM}
    
    print(f"{style_map.get(style)}{color_map.get(color)}{background_map.get(background, '')}{text}{Style.RESET_ALL}", end=end)


def buffer_screen(duration: float, interval: float) -> None:
    """Display a loading screen with spinning characters."""
    buffer_chars = ['|', '/', '-', '\\']
    for _ in range(int(duration // interval)):
        for char in buffer_chars:
            sys.stdout.write(f'\rLoading {char}')
            sys.stdout.flush()
            time.sleep(interval)
    sys.stdout.write('\r' + ' ' * 15 + '\r')
    sys.stdout.flush()


def display_help() -> None:
    """Display help table of Morse alphabet."""
    print(("+" + "-"*11)*5 + '+')
    for i in range(0, 30, 5):
        print('|', end=' ')
        for j in range(5):
            index = i + j
            if index < 30:
                if index < 26:
                   letter = chr(ord('A') + index)
                   morse_code = morse_alphabet[letter]
                else:
                    letter = ' '
                    morse_code = ' '
                print(f"{letter:<2}: {morse_code:<5}", end=" | " if j < 4 else " |")
        print()
    print(("+" + "-"*11)*5 + '+\n')

def display_errors(morse_map:dict, errors:dict, word_list:list, morse_list:list) -> None:
    """Displays the errors after guessing a word."""
    word_errors = {}
    for pos, error in errors.items():
        for word_index, (start_pos, end_pos) in morse_map.items():
            if start_pos <= pos <= end_pos:
                if word_index not in word_errors:
                    word_errors[word_index] = []
                word_errors[word_index].append(error)
                break
            
    e_key = list(errors.keys())[::-1]
    counter = 0
    for w, e in word_errors.items().__reversed__():
        if w % 2 != 0:
            if len(word_list) != 1:
                print(f"In the word '{word_list[w-1]}' written as '{morse_list[w-1]}':")
                for i in e:
                    print(f'  •{i} at position {e_key[counter] - morse_map[w][0] + 1}')
                    counter += 1
            else:
                for i in e:
                    print(f'•{i} at position {e_key[counter]}')
                    counter += 1
        
        else:
            print(f"You forgot a '/' after the word '{word_list[w-2]}':")
        print()

def count_matching_words(sentence1: str, sentence2: str) -> int:
    """Returns the number of matching words between sentence1 and sentece2"""
    return len(set(sentence1.lower().split(' / ')) & set(sentence2.lower().split(' / ')))

def display_user_stats(username:str, stats) -> None:
    """Displays the stats of the given user"""
    if stats:
        print_ct("\n" + "=" * 40, color='cyan')
        print_ct(f"       Welcome, {username.capitalize()}!", color='green')
        print_ct("=" * 40, color='cyan')
        print_ct("      Current Stats:", color='yellow')
        print_ct(f"       Games Played: {stats[0]}", color='white')
        print_ct(f"       Games Won: {stats[1]}", color='white')
        print_ct(f"       Total Score: {stats[2]}", color='white')
        print_ct(f"       Accuracy: {stats[3]*100:.2f}%", color='white')
        print_ct(f"       Max Streak: {stats[6]}", color='white')
        print_ct(f"       Correct Morse Words: {stats[4]}", color='white')
        print_ct(f"       Mistakes: {stats[5]}", color='white')
        print_ct("=" * 40 + "\n", color='cyan')
    

import winsound
from colorama import Fore, Back, Style, init
import time
import re
import sys

morse_alphabet = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--.."
}

def text_to_morse(para: str, key=morse_alphabet):
    return ' '.join(key.get(char.upper(), char) if char != ' ' else '/' for char in para)

def morse_to_sound(morse_para, lenght, freq=500):
    for i in morse_para:
        match i:
            case ".":
                winsound.Beep(freq, lenght)
            case "-":
                winsound.Beep(freq, lenght*3)
            case " ":
                time.sleep(3*lenght/1000)
            case "/":
                time.sleep(lenght/1000)
            case _:
                pass
            
def levenshtein_with_operations(sA, word, sB):
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
    operations = []
    while i > 0 or j > 0:
        if i > 0 and dp[i][j] == 1 + dp[i - 1][j]:
            operations.append(f"You Forgot \"{s1[i - 1]}\"" + ((f" in the word \"{get_word_from_index(sA, i, '/')}\"" if s1[i-1] != '/' else f" after the word \"{get_word_from_index(sA, i-1, '/')}\"") if len(word.split()) != 1 else f" at position '{i}'"))
            i -= 1
        elif j > 0 and dp[i][j] == 1 + dp[i][j - 1]:
            operations.append(f"You added an extra \"{s2[j-1]}\" after \"{s1[i-1]}\"" + (f" in the word \"{get_word_from_index(sA, i, '/')}\"" if len(word.split()) != 1 else f" at position '{i}'"))
            j -= 1
        else:
            if s1[i - 1] != s2[j - 1]:
                operations.append(f"You wrote \"{s2[j-1]}\" instead of \"{s1[i-1]}\"" + (f" in the word \"{get_word_from_index(sA, i, '/')}\"" if len(word.split()) != 1 else f" at position '{i}'"))
            i -= 1
            j -= 1

    return dp[len_s1][len_s2], operations[::-1]

def get_word_from_index(sentence:str, index, separator):
    words = re.split(f'({re.escape(separator)})', sentence)
    words = [item for item in words if item]
    al = []
    for i in words:
        al.append(i.strip().split(' '))
    d = {}
    p = 0
    for j, i in enumerate(al):
        d.update({(j+1): (p+1, p+len(i))})
        p += len(i)
    for word_index, (start, end) in d.items():
        if start <= index <= end:
            return words[word_index-1]
    return None

def print_colored_text(text, color='white', background=None, style='normal', end='\n'):
    color_map = {
        'black': Fore.BLACK,
        'red': Fore.RED,
        'green': Fore.GREEN,
        'yellow': Fore.YELLOW,
        'blue': Fore.LIGHTBLUE_EX,
        'magenta': Fore.MAGENTA,
        'cyan': Fore.CYAN,
        'white': Fore.WHITE,
    }
    
    background_map = {
        'black': Back.BLACK,
        'red': Back.RED,
        'green': Back.GREEN,
        'yellow': Back.YELLOW,
        'blue': Back.BLUE,
        'magenta': Back.MAGENTA,
        'cyan': Back.CYAN,
        'white': Back.WHITE,
    }
    
    style_map = {
        'normal': Style.RESET_ALL,
        'bold': Style.BRIGHT,
        'dim': Style.DIM,
    }

    text_color = color_map.get(color, Fore.WHITE)
    text_background = background_map.get(background, '')
    text_style = style_map.get(style, Style.RESET_ALL)

    formatted_text = f"{text_style}{text_color}{text_background}{text}{Style.RESET_ALL}"

    print(formatted_text, end=end)

def buffer_screen(lenght, omega):
    buffer_chars = ['|', '/', '-', '\\']
    for _ in range(int(lenght//omega)):
        for char in buffer_chars:
            sys.stdout.write('\rLoading ' + char)
            sys.stdout.flush()
            time.sleep(omega)  
    sys.stdout.write('\r')  
    sys.stdout.write(' ' * 15)
    sys.stdout.write('\r')  
    sys.stdout.flush()
    
def help_command():
    print(("+" + "-"*12)*5+'+')
    for i in range(0, 26, 5):
        print('|', end=' ')
        for j in range(5):
            index = i + j
            if index < 26:
                letter = chr(ord('A') + index)
                morse_code = morse_alphabet[letter]
                print("{:<2}:  {:<5}".format(letter, morse_code), end=" ")
                if j < 4:
                    print("|", end=" ")
            if j == 4 and i != 25:
                print("|", end='')
        print()
    print(("+" + "-"*12)*5+'+\n')

    
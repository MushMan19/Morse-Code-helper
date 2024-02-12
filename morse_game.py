from wonderwords import RandomWord, RandomSentence
from morse_code import *
import random
import re
import colorama

def listen(word:str, morse_word:str, lenght=100):
    buffer_screen(0.6, 0.2)
    print_colored_text(f"Type this Morse Code in English ", color='cyan',style='bold', end='')
    print_colored_text("(type 'help' if you're stuck, 're' to listen again or 'back' to go to game selection) ", style='dim')
    morse_to_sound(morse_word, lenght)
    print("Your answer: ",end='')
    user_input = input()
    while user_input == 're':    
        morse_to_sound(morse_word, lenght)
        print("Your answer: ",end='')
        user_input = input()
    
    while user_input == 'help':
        help_command()
        print("Your answer: ",end='')
        user_input = input()
        
    if user_input.strip().lower() == 'back':
        print()
        print()
        return False
    elif user_input == word:
        print_colored_text("Correct!", color='green', style='bold', end=" ")
        print_colored_text("and the Morse Code is", color='green', end=" ")
        print_colored_text(f"\"{morse_word}\"", color="yellow", style='bold')        
    else:
        print_colored_text("Incorrect!", color='red', style='bold', end=" ")
        print_colored_text("The right Word is", color='red', end=" ")
        print_colored_text(f"\"{word.upper()}\"", color="yellow", style='bold', end=" ")        
        print_colored_text("and the Morse code is", color='red', end=" ")
        print_colored_text(f"\"{morse_word}\"", color="yellow", style='bold')        

def t_type(word:str, morse_word:str, pattern:str):
    print_colored_text(f"Type this in Morse Code: ", color='cyan',style='bold', end='')
    print_colored_text(f"\"{word}\"", color='yellow')
    print("Enter your answer: ", end="")
    print_colored_text("(type 'help' if you're stuck or 'back' to go to game selection): ", style='dim',end="")
    user_input = input()
    while user_input == 'help':
        help_command()
        print("Enter your answer: ", end="")
        # print_colored_text("(type 'back' to go to game selection): ", style='dim',end="")
        user_input = input()

        
    if user_input.strip().lower() == 'back':
        print()
        print()
        return False
    
    elif user_input == "":
        print_colored_text("Please try entering something next time", color='magenta')
    elif not re.match(pattern, user_input):
        print_colored_text("Please try entering the answer only in Morse code next time.", color='magenta')
    
    elif user_input == morse_word:
        print_colored_text("Correct!", color='green', style='bold')
    else:
        _, mistakes = levenshtein_with_operations(morse_word, word, user_input)
        print_colored_text("Incorrect!", color='red', style='bold', end=" ")
        print_colored_text("The right Morse Word is", color='red', end=" ")
        print_colored_text(f"\"{morse_word}\"", color="yellow", style='bold')
        for operation in mistakes:
            print("•", end=" ")
            print(operation)


def game():
    colorama.init()
    print_colored_text("""
    ***********************************************
    *                Morse Code Game              *
    *            Welcome to the Challenge!        *
    ***********************************************
    """)
    while True:
        print_colored_text("Choose a game mode", color='blue', style='bold', end=" ")
        print_colored_text("(type 'listen' or 'type' or ('quit' to exit)): ", style='dim', end="")
        game_mode = input().lower()
        if game_mode == 'help':
            help_command()
        elif game_mode.strip().lower() == "quit":
            print('Good Bye! Happy Morse learning')
            colorama.deinit()
            break
        
        elif game_mode.lower().strip() not in ['listen', 'type']:
            print_colored_text("Invalid input. Please enter 'listen' or 'type'.\n", color='magenta')
        
        else:
            cont = True
            allowed_chars = "-./ "
            pattern = f'^[{allowed_chars}]+$'
            
            while True:
                t_word = random.choice([RandomWord().word(), RandomSentence().bare_bone_sentence()])
                result_string = re.sub(r'[^a-zA-Z\s]', '', t_word)
                word = re.sub(r'\s+', ' ', result_string).strip().lower()
                morse_word = text_to_morse(word)
                print()
                if game_mode == "listen":
                    cont = listen(word, morse_word)
                else:
                    cont = t_type(word, morse_word, pattern)
                
                if cont == False: 
                    break

            
if __name__ == "__main__":
    game()

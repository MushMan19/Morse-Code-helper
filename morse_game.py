from wonderwords import RandomWord, RandomSentence
from sys import stdout
from morse_code import *
from database import *
import random
import re
import colorama

# Constants
ALLOWED_CHARS = "-./ "
PATTERN = f'^[{ALLOWED_CHARS}]+$'
CORRECT_POINTS = 40
INCORRECT_POINTS = 10

def listen(word: str, morse_word: str, length=100) -> bool:
    """Handle the 'listen' game mode where users decode Morse code."""
    global stats
    used_help = False
    buffer_screen(0.6, 0.2)

    print_ct("Type this Morse Code in English ", color='cyan', style='bold', end=' ')
    stdout.flush()
    morse_to_sound(morse_word, length)
    user_input = input("Your answer: ").strip().lower()

    while user_input == 're':
        morse_to_sound(morse_word, length)
        user_input = input("Your answer: ").strip().lower()

    while user_input == 'help':
        display_help()
        used_help = True
        stats[6] = 0
        user_input = input("Your answer: ").strip().lower()

    while not user_input:
        print_ct("Please try entering something.", color='magenta')
        user_input = input("Enter your answer: ").strip().lower()

    if user_input == 'back':
        print_ct("=" * 40 + "\n", color='cyan')
        return False
    
    elif user_input == word:
        print_ct("Correct!", color='green', style='bold', end=" ")
        print_ct("and the Morse Code is", color='green', end=" ")
        print_ct(f"\"{morse_word}\"", color="yellow", style='bold')

        if not used_help:
            stats[1] += 1  # Increment games won
            stats[2] += CORRECT_POINTS  # Increment total score
            stats[6] += 1  # Increment current streak

    else:
        _, mistakes = levenshtein_with_operations(morse_word, user_input)
        print_ct("Incorrect!", color='red', style='bold', end=" ")
        print_ct(f"The correct word is \"{word.upper()}\"", color="yellow", style='bold', end=' ')
        print_ct(f"and the Morse code is \"{morse_word}\"", color="yellow", style='bold')


        if not used_help:
            stats[2] -= INCORRECT_POINTS  # Decrement total score
            stats[5] += len(mistakes)  # Increment mistakes count
        
        stats[6] = 0  # Reset current streak
    
    stats[4] += count_matching_words(word, user_input)  # Update matched words count
    return True

def t_type(word: str, morse_word: str) -> bool:
    global stats
    """Handle the 'type' game mode where users encode words into Morse code."""
    print_ct(f"Type this in Morse Code: \"{word}\"", color='cyan', style='bold')

    used_help = False
    user_input = input("Enter your answer: ").strip()

    while user_input == 'help':
        display_help()
        used_help = True
        stats[6] = 0
        user_input = input("Enter your answer: ").strip()
    
    while not user_input:
        print_ct("Please try entering something.", color='magenta')
        user_input = input("Enter your answer: ").strip()
    
    if not re.match(PATTERN, user_input):
        print_ct("Please use only valid Morse code characters.", color='magenta')
      
    elif user_input == 'back':
        print_ct("=" * 40 + "\n", color='cyan')
        return False

    
    elif user_input == morse_word:
        print_ct("Correct!", color='green', style='bold')

        if not used_help:
            stats[1] += 1  # Increment games won
            stats[2] += CORRECT_POINTS  # Increment total score
            stats[6] += 1  # Increment current streak

    else:
        num, mistakes = levenshtein_with_operations(morse_word, user_input)
        m_map, m_list = word_map(morse_word, '/')
        _, w_list = word_map(word, ' ', morse=False)
        
        print_ct("Incorrect!", color='red', style='bold', end=" ")
        print_ct(f"The correct Morse code for \"{word.upper()}\" is \"{morse_word}\"", color="yellow", style='bold')

        print(f'You have made the following {num} mistakes')
        display_errors(m_map, mistakes, w_list, m_list)
        
        if not used_help:
            stats[2] -= INCORRECT_POINTS  # Decrement total score
            stats[5] += len(mistakes)  # Increment mistakes count
        
        stats[6] = 0  # Reset current streak
    
    stats[4] += count_matching_words(morse_word, user_input)  # Update matched words count
    return True

def game() -> None:
    """Main game loop allowing users to select game mode."""
    global stats
    colorama.init()
    
    # Database connection setup
    conn = create_connection("localhost", "root", "1234", "morse")
    if conn is None:
        print_ct("Failed to connect to the database. Exiting game.", color='red', style='bold')
        return
    
    conn.database = "morse"
    create_user_table(conn)

    # User selection or creation
    while True:
        print_ct("Welcome! Please enter your username: ", color='cyan', style='bold', end=" ")
        username = input().strip().lower()
        
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user:
            break
        else:
            print_ct(f"User '{username}' not found. Would you like to create a new user? (y/n): ", color='yellow', style='bold', end=" ")
            create_user_choice = input().strip().lower()
            
            if create_user_choice == 'y':
                add_user(conn, username)
                print_ct(f"User '{username}' created!", color='green', style='bold')
                break
            else:
                print_ct("Please enter a valid username or create a new user.", color='magenta')

    in_stats = get_user_stats(conn, username)
    display_user_stats(username, in_stats)

    stats = [0, 0, 0, 0, 0, 0, 0]  # Initialize game stats

    print_ct("""
    ***********************************************
    *                Morse Code Game              *
    *            Welcome to the Challenge!        *
    ***********************************************
    """, color='cyan', style='bold')

    while True:
        print_ct("Choose a game mode: ", color='blue', style='bold', end=" ")
        print_ct("(type 'listen' or 'type' or 'quit' to exit) ", style='dim', end=" ")
        game_mode = input().strip().lower()

        if game_mode == 'help':
            display_help()
        
        elif game_mode in ['quit', 'exit']:
            update_user_stats(conn, username, *stats)  # Update user stats before quitting
            print(f"Stats updated for user {username.capitalize()}.")
            print_ct('Goodbye! Happy Morse learning!', color='green', style='bold')
            colorama.deinit()
            break
        
        elif game_mode not in ['listen', 'type']:
            print_ct("Invalid input. Please enter 'listen' or 'type'.\n", color='magenta')
        
        else:
            print_ct("(type 'help' if you're stuck or 'back' to go to game selection) ", style='dim')
            while True:
                t_word = random.choice([RandomWord().word(), RandomSentence().bare_bone_sentence()])
                word = re.sub(r'[^a-zA-Z\s]', '', t_word).strip().lower()  # Cleaned word
                morse_word = text_to_morse(word)
                print()

                if game_mode == 'listen':
                    if not listen(word, morse_word):
                        break
                elif game_mode == 'type':
                    if not t_type(word, morse_word):
                        break
                
                stats[0] += 1  # Increment games played

if __name__ == "__main__":
    game()

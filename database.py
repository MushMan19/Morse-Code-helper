import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name=None):
    """Create a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        if connection.is_connected():
            print("Connection successful!")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_database(connection, db_name):
    """Create a new database if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.close()

def create_user_table(connection):
    """Create a table for storing user profiles and stats."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            games_played INT DEFAULT 0,
            games_won INT DEFAULT 0,
            total_score INT DEFAULT 0,
            accuracy FLOAT DEFAULT 0.0,
            morse_words_correct INT DEFAULT 0,
            mistakes INT DEFAULT 0,
            max_streak INT DEFAULT 0
        );
    """)
    cursor.close()

def add_user(connection, username):
    """Add a new user to the users table."""
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO users (username) VALUES (%s);
    """, (username,))
    connection.commit()
    cursor.close()

def update_user_stats(connection, username, games_played=0, games_won=0, total_score=0, 
                      accuracy=0.0, morse_words_correct=0, mistakes=0, max_streak=0):
    """Update user stats after a game."""
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE users
        SET games_played = games_played + %s,
            games_won = games_won + %s,
            total_score = total_score + %s,
            morse_words_correct = morse_words_correct + %s,
            mistakes = mistakes + %s,
            max_streak = GREATEST(max_streak, %s)
        WHERE username = %s;
    """, (games_played, games_won, total_score, morse_words_correct, mistakes, max_streak, username))
    
    cursor.execute("""
        UPDATE users
        SET accuracy = games_won / NULLIF(games_played, 0)  -- Prevent division by zero
        WHERE username = %s;
    """, (username,))
    
    connection.commit()
    cursor.close()

def get_user_stats(connection, username):
    """Retrieve user stats for a specific username."""
    cursor = connection.cursor()
    cursor.execute("""
        SELECT games_played, games_won, total_score, accuracy, morse_words_correct, mistakes, max_streak
        FROM users WHERE username = %s;
    """, (username,))
    stats = cursor.fetchone()
    cursor.close()
    if stats:
        return stats
    else:
        return None

import mysql.connector
from mysql.connector import Error

def create_connection(host_name, user_name, user_password, db_name=None):
    """Create a connection to the MySQL database."""
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            password=user_password,
            database=db_name
        )
        if connection.is_connected():
            print("Connection successful!")
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def create_database(connection, db_name):
    """Create a new database if it doesn't exist."""
    cursor = connection.cursor()
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
    cursor.close()

def create_user_table(connection):
    """Create a table for storing user profiles and stats."""
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            games_played INT DEFAULT 0,
            games_won INT DEFAULT 0,
            total_score INT DEFAULT 0,
            accuracy FLOAT DEFAULT 0.0,
            morse_words_correct INT DEFAULT 0,
            mistakes INT DEFAULT 0,
            max_streak INT DEFAULT 0
        );
    """)
    cursor.close()

def add_user(connection, username):
    """Add a new user to the users table."""
    cursor = connection.cursor()
    cursor.execute("""
        INSERT INTO users (username) VALUES (%s);
    """, (username,))
    connection.commit()
    cursor.close()

def update_user_stats(connection, username, games_played=0, games_won=0, total_score=0, 
                      accuracy=0.0, morse_words_correct=0, mistakes=0, max_streak=0):
    """Update user stats after a game."""
    cursor = connection.cursor()
    cursor.execute("""
        UPDATE users
        SET games_played = games_played + %s,
            games_won = games_won + %s,
            total_score = total_score + %s,
            morse_words_correct = morse_words_correct + %s,
            mistakes = mistakes + %s,
            max_streak = GREATEST(max_streak, %s)
        WHERE username = %s;
    """, (games_played, games_won, total_score, morse_words_correct, mistakes, max_streak, username))
    
    cursor.execute("""
        UPDATE users
        SET accuracy = games_won / NULLIF(games_played, 0)  -- Prevent division by zero
        WHERE username = %s;
    """, (username,))
    
    connection.commit()
    cursor.close()

def get_user_stats(connection, username):
    """Retrieve user stats for a specific username."""
    cursor = connection.cursor()
    cursor.execute("""
        SELECT games_played, games_won, total_score, accuracy, morse_words_correct, mistakes, max_streak
        FROM users WHERE username = %s;
    """, (username,))
    stats = cursor.fetchone()
    cursor.close()
    if stats:
        return stats
    else:
        return None


import sqlite3

def create_connection():
    """Create a connection to the SQLite database."""
    connection = sqlite3.connect('mydatabase.db')
    return connection

def create_tables():
    """Create the necessary tables in the database if they don't already exist."""
    connection = create_connection()
    cursor = connection.cursor()

    # Create table for goals
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        goal_name TEXT NOT NULL,
        goal_description TEXT,
        goal_due_date TEXT,
        goal_priority TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    # Create table for habits
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS habits (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        habit_name TEXT NOT NULL,
        habit_description TEXT,
        habit_frequency TEXT,
        FOREIGN KEY(user_id) REFERENCES users(id)
    )''')

    # Create table for users (if not already created)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )''')

    connection.commit()
    connection.close()

def add_user(username, email, password):
    """Add a new user to the database."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO users (username, email, password)
    VALUES (?, ?, ?)
    ''', (username, email, password))

    connection.commit()
    connection.close()

def get_all_users():
    """Get all users from the database."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    connection.close()
    return users

def add_goal(user_id, goal_name, goal_description, goal_due_date, goal_priority):
    """Add a new goal to the database."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO goals (user_id, goal_name, goal_description, goal_due_date, goal_priority)
    VALUES (?, ?, ?, ?, ?)
    ''', (user_id, goal_name, goal_description, goal_due_date, goal_priority))

    connection.commit()
    connection.close()

def get_goals_by_user(user_id):
    """Get all goals for a specific user."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
    SELECT * FROM goals WHERE user_id = ?
    ''', (user_id,))
    goals = cursor.fetchall()

    connection.close()
    return goals

def add_habit(user_id, habit_name, habit_description, habit_frequency):
    """Add a new habit to the database."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
    INSERT INTO habits (user_id, habit_name, habit_description, habit_frequency)
    VALUES (?, ?, ?, ?)
    ''', (user_id, habit_name, habit_description, habit_frequency))

    connection.commit()
    connection.close()

def get_habits_by_user(user_id):
    """Get all habits for a specific user."""
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute('''
    SELECT * FROM habits WHERE user_id = ?
    ''', (user_id,))
    habits = cursor.fetchall()

    connection.close()
    return habits

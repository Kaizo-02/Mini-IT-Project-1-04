from database import create_connection
import sqlite3

def get_connection():
    conn = sqlite3.connect('your_database.db', check_same_thread=False)  # Set check_same_thread=False for multi-threading support
    return conn

def add_user (username, email, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)",
                   (username, email, password))
    conn.commit()
    conn.close()

def get_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    conn.close()
    return users

def add_goal(user_id, goal, description, due_date):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO goals (user_id, goal, description, due_date)
        VALUES (?, ?, ?, ?)
    """, (user_id, goal, description, due_date))
    conn.commit()
    conn.close()

def get_goals(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM goals WHERE user_id = ?", (user_id,))
    goals = cursor.fetchall()
    conn.close()
    return goals

def add_habit(description, habit_name, user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO habits (description, habit_name, user_id)
        VALUES (?, ?, ?)
    """, (description, habit_name, user_id))
    conn.commit()
    conn.close()

def get_habits(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM habits WHERE user_id = ?", (user_id,))
    habits = cursor.fetchall()
    conn.close()
    return habits

def add_timers(task_name, start_time, end_time, duration, completed, user_id):
    try:
        # Code that might raise an exception (e.g., database insert)
        conn = sqlite3.connect('your_database.db', check_same_thread=False)
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO timers (user_id, task_name, start_time, end_time, duration, completed)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, task_name, start_time, end_time, duration, completed))
        conn.commit()

    except sqlite3.Error as e:
        print(f"Error inserting timer: {e}")

    finally:
        conn.close()

def timers(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM timers WHERE user_id = ?", (user_id,))
    sessions = cursor.fetchall()
    conn.close()
    return sessions




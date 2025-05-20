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

DATABASE = 'mydatabase.db'

def create_connection():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def user_exists(user_id: int) -> bool:
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM users WHERE id = ?", (user_id,))
            return cursor.fetchone() is not None
    except sqlite3.Error as e:
        print(f"Error checking user existence: {e}")
        return False

def add_timers(task, start_time, end_time, duration, completed, user_id):
    print(f"DEBUG: Inserting timer for user {user_id} task '{task}'")
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO timers (task, start_time, end_time, duration, completed, user_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (task, start_time, end_time, duration, completed, user_id))
            conn.commit()
        print("DEBUG: Timer inserted successfully")
    except Exception as e:
        print("DEBUG: Failed to insert timer:", e)


def timers(user_id: int):
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM timers WHERE user_id = ?", (user_id,))
            sessions = cursor.fetchall()
        return sessions
    except sqlite3.Error as e:
        print(f"Error fetching timers: {e}")
        return []

def save_timer_mode(mode_name: str, focus_duration: int, rest_duration: int, user_id: int):
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR IGNORE INTO timer_modes (mode_name, focus_duration, rest_duration, user_id)
                VALUES (?, ?, ?, ?)
            """, (mode_name, focus_duration, rest_duration, user_id))
            conn.commit()
        print(f"Saved timer mode '{mode_name}' for user {user_id}")
    except Exception as e:
        print("Error saving timer mode:", e)

def load_timer_modes(user_id: int):
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT mode_name, focus_duration, rest_duration FROM timer_modes WHERE user_id = ?
            """, (user_id,))
            rows = cursor.fetchall()
        return {row[0]: [("Focus", row[1]), ("Rest", row[2])] for row in rows}
    except Exception as e:
        print("Error loading timer modes:", e)
        return {}
    
def save_user_settings(user_id, background_color, font_family, font_size):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT OR REPLACE INTO settings (user_id, background_color, font_family, font_size)
            VALUES (?, ?, ?, ?)
        ''', (user_id, background_color, font_family, font_size))
        conn.commit()

def load_user_settings(user_id):
    with create_connection() as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT background_color, font_family, font_size FROM settings WHERE user_id = ?
        ''', (user_id,))
        settings = cursor.fetchone()
        if settings:
            return settings
        else:
            # Default settings if no settings found
            return ("white", "Inter", 12)




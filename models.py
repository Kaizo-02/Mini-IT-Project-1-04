import sqlite3
from datetime import datetime

def create_connection():
    conn = sqlite3.connect('mydatabase.db', check_same_thread=False)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def create_tables():
    with create_connection() as conn:
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                email TEXT UNIQUE,
                password TEXT NOT NULL,
                last_user INTEGER DEFAULT 0
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                goal TEXT NOT NULL,
                due_date DATE NOT NULL,
                description TEXT,
                goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habits (
                habit_id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                habit_name TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS timer_modes (
                mode_id INTEGER PRIMARY KEY AUTOINCREMENT,
                mode_name TEXT NOT NULL,
                focus_duration INTEGER NOT NULL,
                rest_duration INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                user_id INTEGER PRIMARY KEY,
                background_color TEXT NOT NULL,
                font_family TEXT NOT NULL,
                font_size INTEGER NOT NULL,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
            goal TEXT NOT NULL,
            due_date DATE NOT NULL,
            description TEXT,
            goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            completion_date DATE,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    print("Database and tables created successfully.")

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
    cursor.execute("SELECT goal_id, goal, description, due_date FROM goals WHERE user_id = ?", (user_id,))
    goals = cursor.fetchall()
    conn.close()
    return goals

    goals_with_status = []
    for goal in goals:
        goal_id, goal_text, description, due_date, completion_date = goal
        due_date = datetime.strptime(due_date, "%Y-%m-%d").date()  # Convert to date object
        status = calculate_goal_status(due_date, completion_date)
        goals_with_status.append({
            "goal_id": goal_id,
            "goal": goal_text,
            "description": description,
            "due_date": due_date,
            "status": status,
            "completion_date": completion_date
        })

    return goals_with_status

def add_completion_date_column():
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE goals ADD COLUMN completion_date DATE")
        conn.commit()
        print("Added completion_date column to goals table.")
    except sqlite3.OperationalError:
        # Column already exists
        print("completion_date column already exists.")
    finally:
        conn.close()

def calculate_goal_status(due_date, completion_date):
    if completion_date:
        return "complete"  # If there's a completion date, the goal is complete
    if due_date < datetime.now().date():
        return "overdue"  # If the goal's due date has passed and not completed, it's overdue
    return "due"  # Otherwise, it's due

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

def delete_goal_from_db(goal_id):
    try:
        conn = create_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM goals WHERE goal_id = ?", (goal_id,))
        conn.commit()
        conn.close()
        print(f"Goal with ID {goal_id} has been deleted successfully.")
    except Exception as e:
        print(f"Error deleting goal: {e}")

def set_last_user(user_id: int):
    """Mark this user as the one to auto-login next time."""
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET last_user = 0")                         # clear any old flags
    cur.execute("UPDATE users SET last_user = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def clear_last_user():
    """Remove any auto-login flag (used on explicit logout)."""
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET last_user = 0")
    conn.commit()
    conn.close()

def get_last_user():
    """Return the row for the user where last_user==1, or None."""
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE last_user = 1")
    row = cur.fetchone()
    conn.close()
    return row

if __name__ == '__main__':
    create_tables()
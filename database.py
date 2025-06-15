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
                last_user INTEGER DEFAULT 0,
                active INTEGER DEFAULT 1
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS goals (
                goal TEXT NOT NULL,
                due_date DATE NOT NULL,
                description TEXT,
                goal_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                completion_date INTEGER DATE,
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
            CREATE TABLE IF NOT EXISTS timers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                task TEXT NOT NULL,
                start_time INTEGER NOT NULL,
                end_time INTEGER NOT NULL,
                duration INTEGER NOT NULL,
                mode TEXT DEFAULT 'work',
                completed INTEGER DEFAULT 1,
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
    # Ensure completion_date is selected
    cursor.execute("SELECT goal_id, goal, description, due_date, completion_date FROM goals WHERE user_id = ?", (user_id,))
    goals_raw = cursor.fetchall() # Renamed to avoid confusion
    conn.close()

    goals_with_status = []
    for goal_data_tuple in goals_raw:
        goal_id, goal_text, description, due_date_str, completion_date_str = goal_data_tuple

        # Convert date strings to date objects for calculation
        due_date_obj = datetime.strptime(due_date_str, "%Y-%m-%d").date()
        completion_date_obj = datetime.strptime(completion_date_str, "%Y-%m-%d").date() if completion_date_str else None

        status = calculate_goal_status(due_date_obj, completion_date_obj)

        goals_with_status.append({
            "goal_id": goal_id,
            "goal": goal_text,
            "description": description,
            "due_date": due_date_str, # Keep as string for consistent UI display (can convert later if needed)
            "status": status,
            "completion_date": completion_date_str # Keep as string for consistent UI display
        })

    # Sort goals: overdue first, then due, then completed, then by due date
    goals_with_status.sort(key=lambda x: (
        0 if x['status'] == 'overdue' else \
        1 if x['status'] == 'due' else \
        2,
        x['due_date']
    ))
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

def update_goal(goal_id, user_id, new_goal_text, new_description, new_due_date_str):
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE goals
                SET goal = ?, description = ?, due_date = ?
                WHERE goal_id = ? AND user_id = ?
            """, (new_goal_text, new_description, new_due_date_str, goal_id, user_id))
            conn.commit()
        print(f"Goal ID {goal_id} updated successfully.")
        return True
    except sqlite3.Error as e:
        print(f"Error updating goal ID {goal_id}: {e}")
        return False

def complete_goal(goal_id: int) -> bool:
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            # Set completion_date to today's date if not already set
            cursor.execute("""
                UPDATE goals
                SET completion_date = ?
                WHERE goal_id = ? AND completion_date IS NULL
            """, (datetime.now().strftime("%Y-%m-%d"), goal_id))
            conn.commit()
            if cursor.rowcount > 0: # Check if any row was updated
                print(f"Goal ID {goal_id} marked as complete.")
                return True
            else:
                print(f"Goal ID {goal_id} was already complete or not found.")
                return False
    except sqlite3.Error as e:
        print(f"Error marking goal ID {goal_id} complete: {e}")
        return False

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

def get_last_user():
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE last_user = 1 LIMIT 1")
            user = cursor.fetchone()
            if user:
                print(f"Last user found: {user}")
                return user
            else:
                print("No last logged-in user found.")
                return None
    except sqlite3.Error as e:
        print(f"Error fetching last user: {e}")
        return None


def get_active_goals_count(user_id: int) -> int:
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT COUNT(*)
            FROM goals
            WHERE user_id = ?
            AND completion_date IS NULL
            AND due_date >= CURRENT_DATE
        """, (user_id,))
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        print(f"Error getting active goals count: {e}")
        return 0
    finally:
        conn.close()

def get_habits_tracked_count(user_id: int) -> int:
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM habits WHERE user_id = ?", (user_id,))
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        print(f"Error getting habits tracked count: {e}")
        return 0
    finally:
        conn.close()

def get_pomodoro_sessions_count(user_id: int) -> int:
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT COUNT(*) FROM timers WHERE user_id = ? AND completed = 1", (user_id,))
        count = cursor.fetchone()[0]
        return count
    except sqlite3.Error as e:
        print(f"Error getting pomodoro sessions count: {e}")
        return 0
    finally:
        conn.close()

def get_total_time_tracked(user_id: int) -> int:
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT SUM(duration) FROM timers WHERE user_id = ? AND completed = 1", (user_id,))
        total_seconds = cursor.fetchone()[0]
        return total_seconds if total_seconds is not None else 0
    except sqlite3.Error as e:
        print(f"Error getting total time tracked: {e}")
        return 0
    finally:
        conn.close()

def format_seconds_to_hm(total_seconds: int) -> str:
    if total_seconds is None:
        return "0h 0m"
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours}h {minutes}m"
    
def get_next_user():
    """ Get the next available user from the database. """
    conn = create_connection()
    cursor = conn.cursor()

    # Query to get the next user (the first available user in the database)
    cursor.execute("SELECT id, username FROM users WHERE active = 1 LIMIT 1")
    next_user = cursor.fetchone()

    conn.close()
    return next_user

def clear_last_user():
    """ Clear the 'last_user' flag for the currently logged-in user. """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET last_user = 0 WHERE last_user = 1")
    conn.commit()
    conn.close()

def set_last_user(user_id):
    """ Mark a specific user as the last logged-in user. """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET last_user = 1 WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()

def set_user_active(user_id: int, active: bool):
    """Toggle whether a user shows up in the switch list."""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET active = ? WHERE id = ?",
        (1 if active else 0, user_id)
    )
    conn.commit()
    conn.close()

def get_active_users():
    """
    Return only users who are still active (i.e. not signed out).
    """
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE active = 1")
    users = cursor.fetchall()
    conn.close()
    return users

def get_username_by_id(user_id: int) -> str:
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else ""

if __name__ == '__main__':
    create_tables()
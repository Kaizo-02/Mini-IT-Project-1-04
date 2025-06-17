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
                appearance_mode TEXT DEFAULT 'System',
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS habit_completions (
                completion_id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                user_id INTEGER NOT NULL,
                completion_date TEXT NOT NULL, -- Stored as 'YYYY-MM-DD'
                FOREIGN KEY(habit_id) REFERENCES habits(habit_id) ON DELETE CASCADE,
                FOREIGN KEY(user_id) REFERENCES users(id)
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS app_settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
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
    conn = None # Initialize conn to None
    try:
        with create_connection() as conn: # Use your context manager
            cursor = conn.cursor()
            # Make sure you select ALL 4 columns: id, username, email, password
            cursor.execute('SELECT id, username, email, password FROM users')
            users = cursor.fetchall()
            return users
    except sqlite3.Error as e:
        print(f"Database error while getting users: {e}")
        return [] # Return an empty list in case of error

def get_username(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    return result[0] if result else None

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

def delete_habit(habit_id, user_id):
    """Deletes a habit and all its associated completions."""
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            # Deletion from habit_completions is handled by ON DELETE CASCADE
            cursor.execute('DELETE FROM habits WHERE habit_id = ? AND user_id = ?', (habit_id, user_id))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error deleting habit: {e}")
        return False

def mark_habit_complete(habit_id, user_id, completion_date):
    """Marks a habit as complete for a specific date."""
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            # Check if already completed for this date
            cursor.execute('SELECT 1 FROM habit_completions WHERE habit_id = ? AND user_id = ? AND completion_date = ?',
                           (habit_id, user_id, completion_date))
            if cursor.fetchone():
                return False # Already marked complete
            cursor.execute('INSERT INTO habit_completions (habit_id, user_id, completion_date) VALUES (?, ?, ?)',
                           (habit_id, user_id, completion_date))
            conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Error marking habit complete: {e}")
        return False

def unmark_habit_complete(habit_id, user_id, completion_date):
    """Unmarks a habit as complete for a specific date."""
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM habit_completions WHERE habit_id = ? AND user_id = ? AND completion_date = ?',
                           (habit_id, user_id, completion_date))
            conn.commit()
            return cursor.rowcount > 0
    except sqlite3.Error as e:
        print(f"Error unmarking habit complete: {e}")
        return False

def get_habit_completions(user_id, habit_id=None):
    """Retrieves completion dates for a specific habit or all habits for a user."""
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            if habit_id:
                cursor.execute('SELECT completion_date FROM habit_completions WHERE user_id = ? AND habit_id = ?',
                               (user_id, habit_id))
            else:
                cursor.execute('SELECT habit_id, completion_date FROM habit_completions WHERE user_id = ?',
                               (user_id,))
            return cursor.fetchall()
    except sqlite3.Error as e:
        print(f"Error fetching habit completions: {e}")
        return 

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

def load_user_settings(user_id):
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT background_color, font_family, font_size FROM settings WHERE user_id = ?
            ''', (user_id,))
            settings = cursor.fetchone()
            if settings:
                return settings
            else:
                return ("white", "Inter", 12)
    except sqlite3.Error as e:
        print(f"Error loading user settings: {e}")
        return ("white", "Inter", 12)

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

def add_total_time_tracked_column_if_not_exists():
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN total_time_tracked INTEGER DEFAULT 0")
        conn.commit()
        print("Column 'total_time_tracked' added to 'users' table.")
    except sqlite3.OperationalError as e:
        if "duplicate column name" in str(e):
            print("Column 'total_time_tracked' already exists.")
        else:
            print(f"Error adding column: {e}")
    finally:
        conn.close()

# Placeholder for other database functions you should have (add_timers, load_timer_modes, save_timer_mode, delete_timer_mode)
def add_timers(task, start_time, end_time, duration, completed, user_id):
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO timers (user_id, task, start_time, end_time, duration, completed)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (user_id, task, start_time, end_time, duration, completed))
            conn.commit()
    except sqlite3.Error as e:
        print(f"Error adding timer: {e}")

def load_timer_modes(user_id):
    modes = {}
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT mode_name, focus_duration, rest_duration FROM timer_modes WHERE user_id = ?', (user_id,))
            rows = cursor.fetchall()
            for row in rows:
                modes[row[0]] = [("Focus", row[1]), ("Rest", row[2])]
    except sqlite3.Error as e:
        print(f"Error loading timer modes: {e}")
    return modes

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
        
def reset_total_time_tracked(user_id):
    conn = sqlite3.connect('mydatabase.db')
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET total_time_tracked = 0 WHERE id = ?", (user_id,))
        conn.commit()
        return True
    except sqlite3.Error as e:
        print(f"Database error during total time reset: {e}")
        return False
    finally:
        conn.close()


def format_seconds_to_hms(total_seconds: int) -> str:
    if total_seconds is None:
        return "00:00:00" # Changed to HH:MM:SS format
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
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

def delete_timers_by_user(user_id):
    try:
        with create_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('DELETE FROM timers WHERE user_id = ?', (user_id,))
            conn.commit()
            # Check how many rows were affected. If 0, maybe no timers existed for user.
            # If > 0, it means deletion was successful.
            if cursor.rowcount > 0:
                return True  # Successfully deleted records
            else:
                # No timers found for this user, or deletion somehow affected 0 rows
                print(f"No timers found or deleted for user_id: {user_id}")
                return True # Consider it a success if nothing to delete
                           # OR return False if you want "failed" when no timers existed
    except sqlite3.Error as e:
        print(f"Database error during timer deletion for user {user_id}: {e}")
        return False # Indicate that an error occurred during deletion

def get_username_by_id(user_id: int) -> str:
    conn = create_connection()
    cur = conn.cursor()
    cur.execute("SELECT username FROM users WHERE id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return row[0] if row else ""

if __name__ == '__main__':
    create_tables()
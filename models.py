from database import create_connection

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

def add_timers(task, start_time, end_time, duration, completed, user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO timers (task, start_time, end_time, duration, completed, user_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (task, start_time, end_time, duration, completed, user_id))
    conn.commit()
    conn.close()

def timers(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM timers WHERE user_id = ?", (user_id,))
    sessions = cursor.fetchall()
    conn.close()
    return sessions




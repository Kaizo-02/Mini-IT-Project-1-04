import sqlite3
from database import create_connection

# --- Users ---
def add_user(username, email, password):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO users (username, email, password)
        VALUES (?, ?, ?)
    ''', (username, email, password))
    conn.commit()
    conn.close()

def get_all_users():
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    conn.close()
    return users

# --- Goals ---
def add_goal(user_id, title, description, due_date, priority):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO goals (user_id, title, description, due_date, priority)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, title, description, due_date, priority))
    conn.commit()
    conn.close()

def get_goals_by_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM goals WHERE user_id = ?', (user_id,))
    goals = cursor.fetchall()
    conn.close()
    return goals

# --- Tasks ---
def add_task(goal_id, task_name):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO tasks (goal_id, task_name)
        VALUES (?, ?)
    ''', (goal_id, task_name))
    conn.commit()
    conn.close()

def get_tasks_by_goal(goal_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM tasks WHERE goal_id = ?', (goal_id,))
    tasks = cursor.fetchall()
    conn.close()
    return tasks

# --- Habits ---
def add_habit(user_id, habit_name, preferred_time=None):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO habits (user_id, habit_name, preferred_time)
        VALUES (?, ?, ?)
    ''', (user_id, habit_name, preferred_time))
    conn.commit()
    conn.close()

def get_habits_by_user(user_id):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM habits WHERE user_id = ?', (user_id,))
    habits = cursor.fetchall()
    conn.close()
    return habits

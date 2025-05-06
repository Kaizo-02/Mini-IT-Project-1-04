import sqlite3

def create_connection():
    conn = sqlite3.connect('mydatabase.db')
    return conn

def create_tables():
    conn = create_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            email TEXT UNIQUE,
            password TEXT NOT NULL
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            goal TEXT NOT NULL,
            due_date TEXT NOT NULL,
            description TEXT UNIQUE,
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
            user_id INTEGER NOT NULL UNIQUE,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS timers (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT NOT NULL,
            duration INTEGER NOT NULL,
            completed INTEGER NOT NULL DEFAULT 1,
            user_id INTEGER NOT NULL UNIQUE,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()
    print("Database and tables created successfully.")

if __name__ == '__main__':
    create_tables()

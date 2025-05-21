import sqlite3
try:
    conn = sqlite3.connect('user_data.db')
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE users ADD COLUMN background_image_path TEXT")
    conn.commit()
    print("Successfully added 'background_image_path' column to 'users' table.")
except sqlite3.Error as e:
    print(f"SQLite error: {e}")
    print("The column might already exist, or the 'users' table might not exist.")
finally:
    if conn:
        conn.close()
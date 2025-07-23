import sqlite3

def initialize_database():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password TEXT NOT NULL,
            stance TEXT DEFAULT 'orthodox'
        )
    ''')
    conn.commit()
    conn.close()

#run setup 
if __name__ == "__main__":
    initialize_database()
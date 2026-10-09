import sqlite3


db = sqlite3.connect("tutorial.db")
cursor = db.cursor()


cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        password TEXT NOT NULL
    )
""")


users = [
    ('admin', 'password123'),
    ('user1', 'letmein'),
    ('user2', 'qwerty'),
    ('jdoe', 'securepass'),
]

cursor.executemany("INSERT INTO users (username, password) VALUES (?, ?)", users)
db.commit()

print("Database initialized with sample data.")


db.close()

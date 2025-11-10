import sqlite3

DB_NAME = "budget_manager.db"

users = [
    ("john_doe", "password123"),
    ("jane_smith", "password456"),
    ("bob_wilson", "password789"),
    ("alice_brown", "password321"),
    ("charlie_davis", "password654")
]

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

for username, password in users:
    cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))

conn.commit()
conn.close()

print("5 users added successfully!")
import sqlite3

DB_NAME = "budget_manager.db"

expenses = [
    ("Chinese Food", "Forgot my lunch", "15.00", "2024-11-10", "Food", 1),
    ("PlayStation 5", "It was on sale", "589.00", "2024-11-09", "Entertainment", 2),
    ("Python Course", "Backend developer course", "150.00", "2024-11-08", "Education", 1),
    ("Groceries", "Weekly shopping", "87.50", "2024-11-11", "Food", 3),
    ("Gas", "Filled up tank", "45.00", "2024-11-11", "Transportation", 1)
]

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

for title, description, amount, date, category, user_id in expenses:
    cursor.execute("INSERT INTO expenses (title, description, amount, date, category, user_id) VALUES (?, ?, ?, ?, ?, ?)", 
                   (title, description, amount, date, category, user_id))

conn.commit()
conn.close()

print("5 expenses added successfully!")
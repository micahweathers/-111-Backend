from flask import Flask, jsonify, request
import sqlite3
from datetime import date

from constants import *
from responses import *


app = Flask(__name__)


DB_NAME = "budget_manager.db"


def init_db():
    conn = sqlite3.connect(DB_NAME) #opens connection to database
    cursor = conn.cursor()#creates a tool called cursor to send commands

#--------|Users Table|---------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    )
""")
    
#--------|Expenses Table|---------
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT NOT NULL,
        amount TEXT NOT NULL,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

    conn.commit()
    conn.close()



@app.get("/api/health")
def health_check():
    return success_response ("API working")


@app.post("/api/register")
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(SQL_INSERT_USER, (username, password))
    conn.commit()
    conn.close()

    return jsonify ({
        "success": True,
        "message": "User Registered Successfully"
    }), 201


@app.post("/api/login")
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    cursor.execute(SQL_LOGIN_USER, (username,))
    user = cursor.fetchone()
    conn.close()

    if user and user["password"] == password:
        return success_response ("User Logged In Successfully", dict(user))

    return jsonify ({
        "success": False,
        "message": "Invalid Credentials"
    }), 401


@app.get("/api/users/<int:user_id>")
def get_user_by_id(user_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(SQL_SELECT_USER_BY_ID, (user_id,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return success_response ("User Retrieved Successfully", dict(user))
    
    return not_found("User")


@app.put("/api/users/<int:user_id>")
def update_user(user_id):
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if user exists first
    cursor.execute(SQL_SELECT_USER_BY_ID, (user_id,))
    if not cursor.fetchone():
        conn.close()

        return not_found("User")
    
    # Update the user
    cursor.execute(SQL_UPDATE_USER, (username, password, user_id))
    
    conn.commit()
    conn.close()
    return success_response ("User Updated Successfully")


@app.delete("/api/users/<int:user_id>")
def delete_user(user_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if user exists first
    cursor.execute(SQL_SELECT_USER_BY_ID, (user_id,))
    if not cursor.fetchone():
        conn.close()
        return not_found("User")

    cursor.execute(SQL_DELETE_USER, (user_id,))
    conn.commit()
    conn.close()

    return success_response ("User Deleted Successfully",)


@app.get("/api/users")
def get_users():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(SQL_SELECT_ALL_USERS)
    rows = cursor.fetchall()
    conn.close()

    users = []

    for row in rows:
        user = {
            "id": row["id"],
            "username": row["username"],
            "password": row["password"]
        }
        users.append(user)

    return success_response("Users Retrieved Successfully", users)


# ---------|Expenses|----------


@app.post("/api/expenses")
def create_expense():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    amount = data.get("amount")
    date_str = date.today()
    category = data.get("category")
    user_id = data.get("user_id")

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(SQL_INSERT_EXPENSES, (title, description, amount, date_str, category, user_id))
    
    conn.commit()
    conn.close()
    return success_response("Expense Created Successfully")


@app.get("/api/expenses")
def get_expenses():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(SQL_SELECT_ALL_EXPENSES)
    rows = cursor.fetchall()
    conn.close()

    expenses = []

    for row in rows:
        expense = {
            "id": row["id"],
            "title": row["title"],
            "description": row["description"],
            "amount": row["amount"],
            "date": row["date"],
            "category": row["category"],
            "user_id": row["user_id"]
        }
        expenses.append(expense)

    return success_response("Expenses Retrieved Successfully", expenses)


@app.get("/api/expenses/<int:expense_id>")
def get_expense_by_id(expense_id):
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(SQL_SELECT_EXPENSES_BY_ID, (expense_id,))
    expense = cursor.fetchone()
    conn.close()

    if expense:
        return success_response("Expense Retrieved Successfully", dict(expense))
    
    return not_found("Expense")


@app.put("/api/expenses/<int:expense_id>")
def update_expense(expense_id):
    data = request.get_json()
    title = data.get("title")
    description = data.get("description")
    amount = data.get("amount")
    date_str = data.get("date")
    category = data.get("category")
    user_id = data.get("user_id")

    # Validate category
    allowed_categories = ["Food", "Education", "Entertainment", "Transportation"]
    if category and category not in allowed_categories:
        return jsonify({
            "success": False,
            "message": f"Invalid category. Allowed values: {', '.join(allowed_categories)}"
        }), 400

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if expense exists first
    cursor.execute(SQL_SELECT_EXPENSES_BY_ID, (expense_id,))
    if not cursor.fetchone():
        conn.close()
        return not_found("Expense")
    
    # Update the expense
    cursor.execute(SQL_UPDATE_EXPENSES, (title, description, amount, date_str, category, user_id, expense_id))
    
    conn.commit()
    conn.close()
    return success_response("Expense Updated Successfully")


@app.delete("/api/expenses/<int:expense_id>")
def delete_expense(expense_id):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Check if expense exists first
    cursor.execute(SQL_SELECT_EXPENSES_BY_ID, (expense_id,))
    if not cursor.fetchone():
        conn.close()
        return not_found("Expense")

    cursor.execute(SQL_DELETE_EXPENSES, (expense_id,))
    conn.commit()
    conn.close()

    return success_response("Expense Deleted Successfully")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
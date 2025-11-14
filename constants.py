#---------| USERS |----------
SQL_SELECT_ALL_USERS = """
SELECT id, username, password
FROM users
"""


SQL_SELECT_USER_BY_ID = """
SELECT id, username
FROM users
WHERE id =?
"""


SQL_INSERT_USER = """
INSERT INTO users (username, password)
VALUES (?,?)
"""

SQL_UPDATE_USER = """
UPDATE users
SET username=?, password=?
WHERE id =?
"""

SQL_DELETE_USER = """
DELETE FROM users
WHERE id =?
"""

SQL_LOGIN_USER = """
SELECT * 
FROM users 
WHERE username = ?
"""
#---------| EXPENSES |----------
SQL_SELECT_ALL_EXPENSES = """
SELECT id, title, description, amount, date, category, user_id
FROM expenses
"""


SQL_SELECT_EXPENSES_BY_ID = """
SELECT id, title, description, amount, date, category, user_id
FROM expenses
WHERE id =?
"""


SQL_INSERT_EXPENSES = """
INSERT INTO expenses (title, description, amount, date, category, user_id)
VALUES (?, ?, ?, ?, ?, ?)
"""

SQL_UPDATE_EXPENSES = """
UPDATE expenses
SET title =?, description =?, amount =?, date =?, category =?, user_id =?
WHERE id =?
"""

SQL_DELETE_EXPENSES = """
DELETE FROM expenses
WHERE id =?
"""
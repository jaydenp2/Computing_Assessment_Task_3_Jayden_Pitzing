import sqlite3 as sql

def listExtension():
  con = sql.connect("database/data_source.db")
  cur = con.cursor()
  data = cur.execute('SELECT * FROM User_Database').fetchall()
  con.close()
  return data

def init_db():
    conn = sql.connect('database/data_source.db')  # Use your actual database filename
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User_Database (
            User_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            First_Name TEXT,
            Surname TEXT,
            Email TEXT UNIQUE NOT NULL,
            Account_Password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def validate_user(email, password):
    email = email.strip()
    password = password.strip()
    conn = sql.connect('database/data_source.db')
    cursor = conn.cursor()
    # Step 1: Check if Email exists and get User_ID
    cursor.execute("SELECT User_ID FROM User_Database WHERE Email = ?", (email,))
    user_row = cursor.fetchone()
    if not user_row:
        conn.close()
        return False
    user_id = user_row[0]
    # Step 2: Check if Account_Password matches for that User_ID
    cursor.execute("SELECT Account_Password FROM User_Database WHERE User_ID = ?", (user_id,))
    password_row = cursor.fetchone()
    conn.close()
    if password_row and password_row[0] == password:
        return True
    return False

def create_user(full_name, email, password):
    conn = sql.connect('database/data_source.db')
    cursor = conn.cursor()
    # Split full name
    parts = full_name.strip().split(' ', 1)
    first_name = parts[0]
    surname = parts[1] if len(parts) > 1 else ''
    # Get next User_ID
    cursor.execute("SELECT MAX(User_ID) FROM User_Database")
    max_id = cursor.fetchone()[0]
    if max_id is None:
        next_id = 1
    else:
        next_id = int(max_id) + 1
    # Insert into User_Database
    cursor.execute(
        "INSERT INTO User_Database (User_ID, First_Name, Surname, Email, Account_Password) VALUES (?, ?, ?, ?, ?)",
        (next_id, first_name, surname, email, password)
    )
    # Insert into User_Time
    cursor.execute(
        "INSERT INTO User_Time (User_ID) VALUES (?)",
        (next_id,)
    )
    conn.commit()
    conn.close()
    return next_id

def get_user_by_email(email):
    conn = sql.connect('database/data_source.db')
    cursor = conn.cursor()
    cursor.execute("SELECT First_Name, Surname, Email FROM User_Database WHERE Email = ?", (email,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {'First_Name': row[0], 'Surname': row[1], 'Email': row[2]}
    return None
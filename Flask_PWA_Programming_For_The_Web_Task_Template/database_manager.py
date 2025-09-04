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
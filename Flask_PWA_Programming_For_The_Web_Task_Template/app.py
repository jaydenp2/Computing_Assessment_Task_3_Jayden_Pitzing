from flask import Flask, request, session, jsonify
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure key

def get_db():
    conn = sqlite3.connect('data_source.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT id FROM user_database WHERE username=? AND password=?", (username, password))
    user = cur.fetchone()
    if user:
        session['user_id'] = user['id']
        return jsonify({'success': True})
    return jsonify({'success': False, 'message': 'Invalid credentials'}), 401

@app.route('/user_info')
def user_info():
    user_id = session.get('user_id')
    if not user_id:
        return jsonify({'error': 'Not logged in'}), 401
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM 'User Time' WHERE user_id=?", (user_id,))
    info = cur.fetchone()
    if info:
        return jsonify(dict(info))
    return jsonify({'error': 'No info found'}), 404

from main import app

if __name__ == "__main__":
    app.run(debug=True)
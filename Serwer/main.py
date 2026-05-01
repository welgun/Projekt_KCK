import sqlite3
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
DB_NAME = 'fitness_app.db'

def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    ''')
    
    admin_exists = conn.execute('SELECT * FROM users WHERE username = ?', ('admin',)).fetchone()
    if not admin_exists:
        hashed_pw = generate_password_hash('test1234')
        conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', ('admin', hashed_pw))
        print("Utworzono konto testowe: admin / test1234")
        
    conn.commit()
    conn.close()

init_db()

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Brak loginu lub hasła"}), 400

    username = data['username']
    password_attempt = data['password']

    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    conn.close()

    if user and check_password_hash(user['password_hash'], password_attempt):
        return jsonify({
            "message": "Zalogowano pomyślnie!",
            "user_id": user['id'],
            "username": user['username']
        }), 200
    else:
        return jsonify({"error": "Nieprawidłowy login lub hasło"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
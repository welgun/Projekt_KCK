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

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Brak loginu lub hasła"}), 400

    username = data['username']
    password = data['password']

    conn = get_db()
    
    existing_user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    
    if existing_user:
        conn.close()
        return jsonify({"error": "Użytkownik o takim loginie już istnieje"}), 409

    hashed_password = generate_password_hash(password)

    try:
        cursor = conn.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', (username, hashed_password))
        conn.commit()
        
        new_user_id = cursor.lastrowid
        
        return jsonify({
            "message": "Zarejestrowano pomyślnie!",
            "user_id": new_user_id,
            "username": username
        }), 201
        
    except sqlite3.Error as e:
        conn.rollback()
        return jsonify({"error": "Błąd bazy danych podczas rejestracji"}), 500
        
    finally:
        conn.close()

@app.route('/api/change_password', methods=['PUT'])
def change_password():
    data = request.get_json()
    
    # Sprawdzamy, czy przesłano wszystkie wymagane pola
    if not data or not data.get('username') or not data.get('old_password') or not data.get('new_password'):
        return jsonify({"error": "Brak nazwy użytkownika, starego lub nowego hasła"}), 400

    username = data['username']
    old_password = data['old_password']
    new_password = data['new_password']

    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    # Weryfikacja: czy użytkownik istnieje i czy stare hasło się zgadza
    if user and check_password_hash(user['password_hash'], old_password):
        new_hashed_password = generate_password_hash(new_password)
        
        try:
            conn.execute('UPDATE users SET password_hash = ? WHERE id = ?', (new_hashed_password, user['id']))
            conn.commit()
            return jsonify({"message": "Hasło zostało zmienione pomyślnie!"}), 200
        except sqlite3.Error:
            conn.rollback()
            return jsonify({"error": "Błąd bazy danych podczas zmiany hasła"}), 500
        finally:
            conn.close()
    else:
        conn.close()
        return jsonify({"error": "Nieprawidłowy login lub aktualne hasło"}), 401


@app.route('/api/delete_account', methods=['DELETE'])
def delete_account():
    data = request.get_json()
    
    if not data or not data.get('username') or not data.get('password'):
        return jsonify({"error": "Brak loginu lub hasła"}), 400

    username = data['username']
    password = data['password']

    conn = get_db()
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()

    # Weryfikacja: potwierdzamy tożsamość przed usunięciem konta
    if user and check_password_hash(user['password_hash'], password):
        try:
            conn.execute('DELETE FROM users WHERE id = ?', (user['id'],))
            conn.commit()
            return jsonify({"message": "Konto zostało trwale usunięte."}), 200
        except sqlite3.Error:
            conn.rollback()
            return jsonify({"error": "Błąd bazy danych podczas usuwania konta"}), 500
        finally:
            conn.close()
    else:
        conn.close()
        return jsonify({"error": "Nieprawidłowy login lub hasło"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
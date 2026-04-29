from flask import Flask, jsonify, request
from flask_wtf.csrf import CSRFProtect # Added import
import sqlite3
import os

app = Flask(__name__)

# SECURITY FIX: Set a secret key for CSRF to work
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-me')

csrf = CSRFProtect()
csrf.init_app(app)

DB_NAME = "aceest_fitness.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn: # Using 'with' handles close() automatically
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS clients (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT UNIQUE, 
                program TEXT,
                status TEXT
            )
        """)
        cur.execute("INSERT OR IGNORE INTO clients (name, program, status) VALUES ('Admin_Test', 'Pro Plan', 'Active')")
        conn.commit()

@app.route('/health', methods=['GET'])
@csrf.exempt # Exempting health check from CSRF
def health_check():
    return jsonify({"status": "ACEest System Online", "version": "1.0.0"}), 200

@app.route('/clients', methods=['GET'])
def get_clients():
    with sqlite3.connect(DB_NAME) as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM clients")
        rows = cur.fetchall()
        clients = [{"id": r[0], "name": r[1], "program": r[2], "status": r[3]} for r in rows]
    return jsonify(clients), 200

@app.route('/add_client', methods=['POST'])
@csrf.exempt # APIs usually exempt CSRF or use Bearer Tokens instead
def add_client():
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    try:
        with sqlite3.connect(DB_NAME) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO clients (name, program, status) VALUES (?, ?, ?)", 
                        (data['name'], data.get('program', 'Basic'), 'Active'))
            conn.commit()
        return jsonify({"message": f"Client {data['name']} added"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Client already exists"}), 409

if __name__ == '__main__':
    init_db()
    # Use 0.0.0.0 if running in Docker, otherwise 127.0.0.1 is fine for local
    app.run(host='0.0.0.0', port=5000, debug=False)
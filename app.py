from flask import Flask, jsonify, request
from flask_wtf.csrf import CSRFProtect
import sqlite3
import os

app = Flask(__name__)

# SECURITY FIX: Remove hard-coded strings to satisfy SonarCloud.
# The app will now pull the key from the K8s environment variable.
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Compliant credential handling via environment variables
username = os.getenv("username") 
password = os.getenv("password") 
# Note: In a real app, you'd use these for DB or API auth
usernamePassword = 'user=%s&password=%s' % (username, password) 

csrf = CSRFProtect()
csrf.init_app(app)

DB_NAME = "/tmp/aceest_fitness.db"

def init_db():
    with sqlite3.connect(DB_NAME) as conn:
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
@csrf.exempt 
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
@csrf.exempt 
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
    # 0.0.0.0 allows the K8s Service to reach the container
    # Set debug=False for production readiness
    app.run(host='0.0.0.0', port=5000, debug=False)
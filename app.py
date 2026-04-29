from flask import Flask, jsonify, request
from flask_wtf.csrf import CSRFProtect
import sqlite3
import os

app = Flask(__name__)

# Pull secret from environment (Injected via K8s Secret)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

# Compliant environment variable handling
username = os.getenv("username") 
password = os.getenv("password") 
usernamePassword = 'user=%s&password=%s' % (username, password) 

csrf = CSRFProtect()
csrf.init_app(app)

# SQLite fix: Move to /tmp so the non-root user has write access
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
# Exempting Health Check is generally okay as it is a GET (safe method)
# but we can remove it to be 100% "Sonar-Clean"
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
# COMPLIANT: Removed @csrf.exempt to satisfy SonarCloud security rules
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
    
    # SONAR FIX: Default to 127.0.0.1 for local safety.
    # K8S FIX: Use an environment variable to switch to 0.0.0.0 in the cluster.
    host = os.getenv("FLASK_RUN_HOST", "127.0.0.1")
    
    app.run(host=host, port=5000, debug=False)
from flask import Flask, jsonify, request
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "aceest_fitness.db"

def init_db():
    """Initializes the SQLite database for a web environment."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT UNIQUE, 
            program TEXT,
            status TEXT
        )
    """)
    # Seed initial data for validation
    cur.execute("INSERT OR IGNORE INTO clients (name, program, status) VALUES ('Admin_Test', 'Pro Plan', 'Active')")
    conn.commit()
    conn.close()

@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint for Jenkins/GitHub Actions to verify service availability."""
    return jsonify({"status": "ACEest System Online", "version": "1.0.0"}), 200

@app.route('/clients', methods=['GET'])
def get_clients():
    """Service endpoint to retrieve all gym members."""
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients")
    rows = cur.fetchall()
    clients = [{"id": r[0], "name": r[1], "program": r[2], "status": r[3]} for r in rows]
    conn.close()
    return jsonify(clients), 200

@app.route('/add_client', methods=['POST'])
def add_client():
    """Endpoint to add new members via JSON payload."""
    data = request.json
    if not data or 'name' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cur = conn.cursor()
        cur.execute("INSERT INTO clients (name, program, status) VALUES (?, ?, ?)", 
                    (data['name'], data.get('program', 'Basic'), 'Active'))
        conn.commit()
        conn.close()
        return jsonify({"message": f"Client {data['name']} added"}), 201
    except sqlite3.IntegrityError:
        return jsonify({"error": "Client already exists"}), 409

if __name__ == '__main__':
    init_db()
    # Bind to 0.0.0.0 to allow Docker port mapping
    app.run(host='0.0.0.0', port=5000)
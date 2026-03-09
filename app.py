from flask import Flask, jsonify, request
import sqlite3
import random

app = Flask(__name__)
DB_NAME = "aceest_fitness.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS clients 
        (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE, program TEXT)""")
    # Seed initial data for testing
    cur.execute("INSERT OR IGNORE INTO clients (name, program) VALUES ('Initial Client', 'Beginner')")
    conn.commit()
    conn.close()

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "ACEest Fitness"}), 200

@app.route('/clients', methods=['GET'])
def get_clients():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM clients")
    clients = [{"id": r[0], "name": r[1], "program": r[2]} for r in cur.fetchall()]
    conn.close()
    return jsonify(clients), 200

@app.route('/generate_program', methods=['POST'])
def generate_program():
    data = request.get_json()
    name = data.get('name')
    programs = ["Fat Loss", "Muscle Gain", "Beginner"]
    selected = random.choice(programs)
    
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("UPDATE clients SET program=? WHERE name=?", (selected, name))
    conn.commit()
    conn.close()
    return jsonify({"name": name, "assigned_program": selected}), 200

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000)
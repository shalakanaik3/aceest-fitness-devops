from flask import Flask, jsonify, request

app = Flask(__name__)

# Mock database for gym members
members = [
    {"id": 1, "name": "John Doe", "plan": "Gold"},
    {"id": 2, "name": "Jane Smith", "plan": "Silver"}
]

@app.route('/')
def home():
    return jsonify({"message": "Welcome to ACEest Fitness & Gym Management System"})

@app.route('/members', methods=['GET'])
def get_members():
    return jsonify(members)

@app.route('/add_member', methods=['POST'])
def add_member():
    new_member = request.json
    members.append(new_member)
    return jsonify(new_member), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
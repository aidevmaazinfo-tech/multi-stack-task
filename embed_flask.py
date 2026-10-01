from flask import Flask, render_template, request, jsonify, session

app = Flask(__name__)
app.secret_key = 'super-secret-key-2024'

users_db = {
    "admin": {"password": "1234", "name": "Administrator"},
    "user": {"password": "pass", "name": "Regular User"}
}

@app.route('/')
def index():
    return render_template('login.html')

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if username in users_db and users_db[username]['password'] == password:
        session['logged_in'] = True
        return jsonify({"success": True, "message": f"Welcome, {users_db[username]['name']}!"})
    return jsonify({"success": False, "message": "Invalid credentials!"}), 401

if __name__ == '__main__':
    app.run(debug=True, port=5000)
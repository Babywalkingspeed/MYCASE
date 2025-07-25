from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from config import Config
from models import create_user, get_user_by_email
from utils import create_token
from werkzeug.security import check_password_hash

app = Flask(__name__)
app.config.from_object(Config)
CORS(app)
bcrypt = Bcrypt(app)
mysql = MySQL(app)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role', 'User')

    if get_user_by_email(mysql, email):
        return jsonify({'message': 'Email already exists'}), 400

    create_user(mysql, email, password, role)
    return jsonify({'message': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = get_user_by_email(mysql, email)
    if user and check_password_hash(user['password'], password):
        token = create_token(user['id'], user['role'])
        return jsonify({'token': token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    # Mock example - add email logic if needed
    data = request.json
    email = data.get('email')
    user = get_user_by_email(mysql, email)
    if user:
        return jsonify({'message': 'Reset link sent to email'}), 200
    return jsonify({'message': 'Email not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)

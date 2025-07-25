from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from config import Config
from models import create_user, get_user_by_emp_code
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
    employee_code = data.get('employee_code')

    if get_user_by_emp_code(mysql, employee_code):
        return jsonify({'message': 'รหัสพนักงานนี้มีอยู่แล้ว'}), 400

    create_user(mysql, data)
    return jsonify({'message': 'ลงทะเบียนสำเร็จ'}), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    employee_code = data.get('employee_code')
    password = data.get('password')

    user = get_user_by_emp_code(mysql, employee_code)
    if user and check_password_hash(user['password'], password):
        token = create_token(user['id'], user['role'])
        return jsonify({
            'token': token,
            'name': f"{user['first_name']} {user['last_name']}",
            'department': user['department'],
            'position': user['position'],
            'role': user['role']
        }), 200
    else:
        return jsonify({'message': 'รหัสพนักงานหรือรหัสผ่านไม่ถูกต้อง'}), 401

@app.route('/forgot-password', methods=['POST'])
def forgot_password():
    # ตัวอย่าง mock ยังใช้ email ค้นหา
    data = request.json
    employee_code = data.get('employee_code')
    user = get_user_by_emp_code(mysql, employee_code)
    if user:
        return jsonify({'message': 'ระบบจะส่งลิงก์ไปยังอีเมลของคุณ (mock)'}), 200
    return jsonify({'message': 'ไม่พบรหัสพนักงานในระบบ'}), 404

if __name__ == '__main__':
    app.run(debug=True)

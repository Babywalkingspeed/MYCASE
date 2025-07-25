import pymysql
from werkzeug.security import generate_password_hash

def create_user(mysql, data):
    hashed_pw = generate_password_hash(data['password'])
    cursor = mysql.connection.cursor()
    cursor.execute("""
        INSERT INTO users (employee_code, first_name, last_name, email, password, department, position, role)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        data['employee_code'],
        data['first_name'],
        data['last_name'],
        data['email'],
        hashed_pw,
        data['department'],
        data['position'],
        data.get('role', 'User')
    ))
    mysql.connection.commit()
    cursor.close()

def get_user_by_emp_code(mysql, emp_code):
    cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE employee_code = %s", (emp_code,))
    user = cursor.fetchone()
    cursor.close()
    return user

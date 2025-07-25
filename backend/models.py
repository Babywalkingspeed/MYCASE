import pymysql
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(mysql, email, password, role):
    hashed_pw = generate_password_hash(password)
    cursor = mysql.connection.cursor()
    cursor.execute("INSERT INTO users  (email, password, role) VALUES (%s, %s, %s)", (email, hashed_pw, role))
    mysql.connection.commit()
    cursor.close()

def get_user_by_email(mysql, email):
    cursor = mysql.connection.cursor(pymysql.cursors.DictCursor)
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    user = cursor.fetchone()
    cursor.close()
    return user

from flask import Flask, request
import sqlite3
import os

app = Flask(__name__)

# 🚨 VULNERABILITY 1: Hardcoded Cloud Secrets
AWS_ACCESS_KEY = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # 🚨 VULNERABILITY 2: Severe SQL Injection (SQLi)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cursor.execute(query)
    
    if cursor.fetchone():
        return "Welcome to the admin panel!"
    return "Login failed."

@app.route('/ping', methods=['GET'])
def ping_server():
    ip_address = request.args.get('ip')
    
    # 🚨 VULNERABILITY 3: Remote Code Execution / Command Injection
    # Never pass user input directly into os.system!
    result = os.system(f"ping -c 1 {ip_address}")
    return f"Ping executed with result: {result}"

if __name__ == '__main__':
    app.run(debug=True)

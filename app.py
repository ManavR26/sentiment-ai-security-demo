from flask import Flask, request, render_template_string, send_file
import sqlite3
import subprocess
import pickle
import hashlib
import os

app = Flask(__name__)

# 🚨 1. SECRETS LEAK (Category: Exposed Credentials)
AWS_SECRET_KEY = os.environ.get('AWS_SECRET_KEY')
GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN')

# 🚨 2. SQL INJECTION (Category: Injection)
@app.route('/user')
def get_user():
    user_id = request.args.get('id')
    conn = sqlite3.connect('app.db')
    cursor = conn.cursor()
    # Vulnerable: Direct string interpolation in SQL query
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")
    return str(cursor.fetchall())

# 🚨 3. COMMAND INJECTION (Category: Remote Code Execution)
@app.route('/ping')
def ping():
    ip = request.args.get('ip')
    # Vulnerable: Unsanitized user input passed directly to the system shell
    subprocess.call(f"ping -c 1 {ip}", shell=True)
    return "Ping executed!"

# 🚨 4. CROSS-SITE SCRIPTING / XSS (Category: Injection)
@app.route('/hello')
def hello():
    name = request.args.get('name', 'Guest')
    # Vulnerable: Rendering user input directly into HTML without escaping it
    template = f"<h1>Welcome to the dashboard, {name}!</h1>"
    return render_template_string(template)

# 🚨 5. INSECURE DESERIALIZATION (Category: Software and Data Integrity Failures)
@app.route('/load_config', methods=['POST'])
def load_config():
    data = request.data
    # Vulnerable: Unpickling untrusted data allows attackers to execute arbitrary code
    config = pickle.loads(data)
    return "Config loaded"

# 🚨 6. PATH TRAVERSAL (Category: Broken Access Control)
@app.route('/download')
def download_file():
    filename = request.args.get('file')
    base_dir = '/var/www/uploads/'
    filepath = os.path.abspath(os.path.join(base_dir, filename))
    if not filepath.startswith(base_dir):
        return "Forbidden", 403
    if not os.path.isfile(filepath):
        return "File not found", 404
    return send_file(filepath)

# 🚨 7. WEAK CRYPTOGRAPHY (Category: Cryptographic Failures)
@app.route('/hash')
def hash_password():
    password = request.args.get('password')
    # Vulnerable: MD5 is a broken hashing algorithm and easily cracked
    hashed = hashlib.md5(password.encode()).hexdigest()
    return hashed

# 🚨 8. SECURITY MISCONFIGURATION (Category: Misconfiguration)
if __name__ == '__main__':
    # Vulnerable: Running Flask in debug mode on a public interface exposes the Werkzeug console
    app.run(host='0.0.0.0', port=5000, debug=True)

import os
import subprocess
import flask

app = flask.Flask(__name__)

# VULNERABILITY 1: Hardcoded API Key (Bandit will scream at this)
AWS_SECRET_KEY = "AKIAIOSFODNN7EXAMPLE" 

# VULNERABILITY 2: SQL Injection Risk
def get_user(user_id):
    # This is bad practice; directly formatting strings into SQL
    query = "SELECT * FROM users WHERE id = " + user_id 
    return query

# VULNERABILITY 3: Command Injection
@app.route('/ping')
def ping():
    address = flask.request.args.get('address')
    # Extremely dangerous: running shell commands from user input
    subprocess.call("ping " + address, shell=True) 

if __name__ == '__main__':
    # VULNERABILITY 4: Debug mode enabled in production
    app.run(debug=True)

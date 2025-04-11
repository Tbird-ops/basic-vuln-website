# This app is intentionally vulnerable and simple to demonstrate old
# web flaws and wireshark analysis
import hashlib
from flask import Flask, render_template, request, url_for, redirect

app = Flask(__name__)
app.secret_key = 'yeet'

# Runtime information
known_accounts = {}
cookies = {}

# Helper functions
def validate_account(loginEmail, loginPassword):
    if loginEmail in known_accounts.keys():
        if known_accounts[loginEmail] == loginPassword:
            return True
        else:
            return False
    else:
        return False

def validate_cookie(cookie):
    if cookie in cookies.keys():
        return True
    else:
        return False

def create_cookie(loginEmail):
    md5 = hashlib.md5(loginEmail.encode('utf-8')).hexdigest()
    cookies[md5] = loginEmail
    return md5

# ROUTES
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/login', methods=['POST'])
def login():
    print(f"Attempted login: USER:{request.form['loginEmail']} PASS:{request.form['loginPassword']}")
    email = request.form['loginEmail']
    password = request.form['loginPassword']
    valid = validate_account(email, password)
    if valid:
        print(f"User {email} logged in successfully")
        md5 = create_cookie(email)
        print(f"User {email} cookie created {md5}")
        response = redirect(url_for('home'))
        response.set_cookie('Session', md5)
        return response
    else:
        print(f"User {request.form['loginEmail']} login failed")
        return render_template("index.html", message="Login failed"), 403

@app.route('/signup', methods=['POST'])
def signup():
    print(f"New Signup: USER:{request.form['signupEmail']} PASS:{request.form['signupPassword']}")
    known_accounts[request.form['signupEmail']] = request.form['signupPassword']
    return render_template("index.html", message="Sign up successful!")

@app.route('/home', methods=['GET'])
def home():
    if validate_cookie(request.cookies.get('Session')):
        return render_template("home.html", user=cookies[request.cookies.get('Session')])
    else:
        return render_template("index.html", message="Please login first!")

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True, port=5000)
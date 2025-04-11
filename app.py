from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Response
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required

# Gunicorn import for Session from flask_session to resolve writing
# import os

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///WeldDB.db")

# Flask Run config for Session from flask_session
# Dockerfile must contain: RUN chown -R appuser /app/flask_session
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

"""
# Gunicorn config for Session from flask_session to resolve writing
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_FILE_DIR"] = "/tmp/flask_session"  # Use a writable dir
app.config["SESSION_TYPE"] = "filesystem"
# Ensure the directory exists
os.makedirs("/tmp/flask_session", exist_ok=True)
Session(app)
"""

#Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Home Page
@app.route("/")
@login_required
def index():
    return '''<h1 style="margin: 0; height: 100vh; display: flex; 
              justify-content: center; align-items: center;">INDEX</h1>'''

# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")

# Register user
@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("login.html")

""" example
@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    return '<h1 style="text-align: center;">Hello, World!</h1>'
"""
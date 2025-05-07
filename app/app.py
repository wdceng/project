from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Response
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required


# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///weld_db.db")

# Flask Run config for Session from flask_session
# Dockerfile must contain: RUN chown -R appuser /app/flask_session
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Set default theme and inject it into all Jinja templates automatically
@app.context_processor
def inject_theme():
    theme = request.args.get("t", "light")
    if theme not in ["dark", "light"]:
        theme = "light"
    return dict(theme=theme)


# Home Page
@app.route("/")
@login_required
def index():
    return '<h1 style="margin: 0; height: 100vh; display: flex; justify-content: center; align-items: center;">INDEX</h1>'


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    return render_template("login.html")


# Register user
@app.route("/register", methods=["GET", "POST"])
def register():
    return render_template("register.html")

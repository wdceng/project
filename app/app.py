from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, redirect_with_theme


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
# Ref. https://flask.palletsprojects.com/en/stable/templating/
@app.context_processor
def inject_theme():
    theme = request.args.get("t", "light")
    if theme not in ["dark", "light"]:
        theme = "light"
    return dict(theme=theme)


# Register user
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get name and password from the form
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()
        confirmation = request.form.get("confirmation").strip()

        # Ensure username was submitted
        if not username:
            flash("Username is required. (Error 400)", "flash-error")
            return render_template("register.html")

        # Ensure password was submitted
        elif not password:
            flash("Password is required. (Error 400)", "flash-error")
            return render_template("register.html")

        # Ensure confirmation was submitted
        elif not confirmation:
            flash("Password confirmation is required. (Error 400)", "flash-error")
            return render_template("register.html")

        # Ensure password matches confirmation
        elif password != confirmation:
            flash("Password and confirmation do not match. (Error 400)", "flash-error")
            return render_template("register.html")

        try:
            # Attempt to insert the new user
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                username,
                generate_password_hash(password),
            )

        except ValueError:
            # Handle the case where the username already exists
            flash(
                "Username already taken. Please choose a different one. (Error 400)",
                "flash-error",
            )
            return render_template("register.html")

        flash("Registration complete. You can now log in.", "flash-success")
        return render_template("login.html")
    else:
        return render_template("register.html")


# Login
@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Get name and password from the form
        username = request.form.get("username").strip()
        password = request.form.get("password").strip()

        # Ensure username was submitted
        if not username:
            flash("Username is required. (Error 403)", "flash-error")
            return render_template("register.html")

        # Ensure password was submitted
        elif not password:
            flash("Password is required. (Error 403)", "flash-error")
            return render_template("register.html")

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", username)

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            flash("Invalid username or password. (Error 403)", "flash-error")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect_with_theme("index")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect_with_theme("login")


# Home Page
@app.route("/")
@login_required
def index():
    return render_template("index.html")

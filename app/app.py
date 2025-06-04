from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import login_required, redirect_with_theme


# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///weld_db.db")

# Flask Run config for Session from flask_session
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


# Home Page
@app.route("/")
@login_required
def index():
    return render_template("index.html")


# Upload Weld Data
@app.route("/upload_weld_data", methods=["GET", "POST"])
@login_required
def welds():
    """Register welds"""
    # List all the field names (must match your form names)
    fields = [
        "drawing_no",
        "revision",
        "spool_no",
        "weld_no",
        "location",
        "weld_type",
        "size",
        "schedule",
        "fabrication_no",
        "root_welders",
        "root_process",
        "balance_welders",
        "fabrication_date",
        "vt",
        "pt",
        "mt",
        "rt",
        "ut",
    ]
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Build a dictionary of field values, stripping whitespace
        data = {field: (request.form.get(field) or "").strip() for field in fields}

        # Simple validation example (you can expand this!)
        if not data["drawing_no"] or not data["weld_no"]:
            flash("Drawing number and weld number are required.", "flash-error")
            return render_template("upload_weld.html", **data)

        # Prepare values in the same order as fields
        values = [data[field] for field in fields]

        # Prepare SQL query
        field_str = ", ".join(fields)
        placeholders = ", ".join(["?"] * len(fields))
        sql = f"INSERT INTO welds ({field_str}) VALUES ({placeholders})"

        # Insert into database (replace db.execute with your database logic)
        try:
            db.execute(sql, *values)
            flash("Weld uploaded successfully.", "flash-success")
            return redirect(url_for("welds"))
        except Exception as e:
            flash(f"Database error: {e}", "flash-error")
            return render_template("upload_weld_data.html", **data)

        """
        # Get all inputs
        drawing_no = request.form.get("drawing_no").strip()
        revision = request.form.get("revision").strip()
        spool_no = request.form.get("spool_no").strip()
        weld_no = request.form.get("weld_no").strip()
        location = request.form.get("location").strip()
        weld_type = request.form.get("weld_type").strip()
        size = request.form.get("size").strip()
        schedule = request.form.get("schedule").strip()
        fabrication_no = request.form.get("fabrication_no").strip()
        root_welders = request.form.get("root_welders").strip()
        root_process = request.form.get("root_process").strip()
        balance_welders = request.form.get("balance_welders").strip()
        fabrication_date = request.form.get("fabrication_date").strip()
        vt = request.form.get("vt").strip()
        pt = request.form.get("pt").strip()
        mt = request.form.get("mt").strip()
        rt = request.form.get("rt").strip()
        ut = request.form.get("ut").strip()
        """

    else:
        return render_template("upload_weld_data.html")


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

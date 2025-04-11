# import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Response
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    # Select portofolio from db stock_portofolio
    portofolio = db.execute("SELECT stock AS symbol, " +
                            "   SUM(shares) AS sum_shares " +
                            "  FROM stock_portofolio WHERE users_id = ? " +
                            " GROUP BY symbol",
                            session["user_id"]
                            )
    # Select cash from DB users
    cash_from_db = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
    cash_balance = cash_from_db[0]["cash"]

    # Calculating grand total
    grand_total = cash_balance

    # Iterate over portofolio, add stock name and sum grand_total
    for stock in portofolio:
        current_stock_info = lookup(stock["symbol"])
        stock["name"] = current_stock_info["name"]
        stock["current_price"] = current_stock_info["price"]
        stock["current_sum"] = stock["current_price"] * stock["sum_shares"]
        grand_total += stock["current_sum"]

    return render_template("index.html", portofolio=portofolio, cash_balance=cash_balance, grand_total=grand_total)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    # Get stock symbol from the form by POST
    if request.method == "POST":

        # Post stock symbol
        symbol = request.form.get("symbol").strip()
        # Check if the symbol is empty
        if not symbol:
            return apology("Input cannot be empty", 400)
        # Check if the symbol is valid (lookup returns None for invalid symbols)
        stock = lookup(symbol)
        if not stock:
            return apology(f'Stock symbol "{symbol}" does not exist', 400)

        # Post number of shares
        shares = request.form.get("shares").strip()

        # Check if float
        try:
            # Ref. https://python-reference.readthedocs.io/en/latest/docs/float/is_integer.html
            if not shares or not float(shares).is_integer():
                return apology(f'"{shares}", must be positive intager', 400)

        except ValueError:
            # Handle the case where the username already exists
            return apology(f'"{shares}", must be positive intager', 400)

        shares = int(shares)
        # Check if input is not a positive integer
        # Ref. https://www.w3schools.com/python/ref_func_isinstance.asp
        if not shares or shares <= 0:
            return apology(f'"{shares}", must be positive intager', 400)

        # Handle stock price, transaction costs
        stock_price = stock["price"]
        transaction_costs = stock_price * shares

        # Select cash from DB users
        cash_from_db = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash_available = cash_from_db[0]["cash"]

        # Check if available cash is enough for transaction costs
        if cash_available < transaction_costs:
            return apology("You can't afford the number of shares at the current price", 400)

        # Cashback calculation
        cashback = cash_available - transaction_costs

        # Update DB users table with cash remaining
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cashback, session["user_id"])

        # Insert DB stock_portofolio with buying stock records
        stock_symbol = stock["symbol"]
        db.execute("INSERT INTO stock_portofolio (users_id, stock, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], stock_symbol, shares, stock_price)

        flash(
            f"You have just bought {stock_symbol} stock, {shares} shares for {usd(transaction_costs)}")
        return redirect("/")
        # return render_template("buy.html")

    else:
        # GET by default:
        return render_template("buy.html")


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    history_db = db.execute("""
                            SELECT stock AS symbol,
                                   shares,
                                   price,
                                   (ABS(shares) * price) AS sum_prices,
                                   timestamp
                              FROM stock_portofolio WHERE users_id = ?
                             ORDER BY timestamp DESC
                            """,
                            session["user_id"]
                            )

    # Iterate over portofolio, add stock name and sum grand_total
    for transaction in history_db:
        stock_info = lookup(transaction["symbol"])
        transaction["name"] = stock_info["name"]
        if transaction["shares"] > 0:
            transaction["action"] = "bought"
        else:
            transaction["action"] = "sold"
        transaction["shares"] = abs(transaction["shares"])

    return render_template("history.html", history_db=history_db)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    """Get stock quote."""
    # Get stock symbol from the form by POST
    if request.method == "POST":

        symbol = request.form.get("symbol").strip()
        # Check if the symbol is empty
        if not symbol:
            return apology("Input cannot be empty", 400)
        # Check if the symbol is valid (lookup returns None for invalid symbols)
        stock = lookup(symbol)
        if not stock:
            return apology(f'Stock symbol "{symbol}" does not exist', 400)

        try:
            return render_template("quoted.html", stock=stock)

        except Exception as e:
            flash(f'Error: "{e}"')
            # Ref. https://flask.palletsprojects.com/en/stable/quickstart/#message-flashing
            app.logger.error(f"Error fetching stock data: {e}")
            return redirect("/quote")  # apology("Wrong stock name.", 400)

    else:
        # GET by default:
        return render_template("quote.html")


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
            return apology("must provide username", 400)

        # Ensure password was submitted
        elif not password:
            return apology("must provide password", 400)

        # Ensure confirmation was submitted
        elif not confirmation:
            return apology("must provide confirmation", 400)

        # Ensure password matches confirmation
        elif password != confirmation:
            return apology("password and confirmation must match", 400)

        try:
            # Attempt to insert the new user
            db.execute("INSERT INTO users (username, hash) VALUES (?, ?)",
                       username, generate_password_hash(password))

        except ValueError:
            # Handle the case where the username already exists
            return apology("Username already taken. Please choose a different one.", 400)

        # Ref https://flask.palletsprojects.com/en/stable/api/#flask.Response
        return Response(render_template("login.html") +
                        '<p style="text-align: center">Registration successful!</p>',
                        content_type="text/html")
    else:
        return render_template("register.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "POST":
        # Post stock symbol
        symbol = request.form.get("symbol").strip()
        # Check if the symbol is empty
        if not symbol:
            return apology("Input cannot be empty", 400)

        # Post number of shares
        shares = request.form.get("shares").strip()
        # Check if input is not a positive integer
        # Ref. https://www.w3schools.com/python/ref_func_isinstance.asp
        if not shares or int(shares) <= 0:
            return apology(f'"{shares}", must be positive intager', 400)

        # Select stock symbol from db stock_portofolio
        db_stock = db.execute("SELECT stock AS symbol, " +
                              "   SUM(shares) AS sum_shares " +
                              "  FROM stock_portofolio WHERE users_id = ? " +
                              " GROUP BY symbol",
                              session["user_id"]
                              )

        # Check if user has this stock and if the user does not own that many shares of the stock
        stock_counter = 0
        for stock in db_stock:
            if stock["symbol"] == symbol:
                stock_counter += 1
                # If the user does not own that many shares of the stock
                if stock["sum_shares"] < int(shares):
                    return apology("User doesn't have enough stocks", 400)

        # If user doesn't has this stock
        if stock_counter == 0:
            return apology("User doesn't have this stock", 400)

        # Select cash from DB users
        cash_from_db = db.execute("SELECT cash FROM users WHERE id = ?", session["user_id"])
        cash_available = cash_from_db[0]["cash"]

        # Check if the symbol is valid (lookup returns None for invalid symbols)
        stock = lookup(symbol)
        if not stock:
            return apology(f'Error fatching "{symbol}", issue {stock}', 400)

        # Handle stock price, transaction costs
        stock_price = stock["price"]
        transaction_profit = stock_price * int(shares)

        # Cashback calculation
        cashback = cash_available + transaction_profit

        # Update DB users table with cash remaining
        db.execute("UPDATE users SET cash = ? WHERE id = ?", cashback, session["user_id"])

        # Insert DB stock_portofolio with selling stock records
        stock_symbol = stock["symbol"]
        sold_shares = -int(shares)
        db.execute("INSERT INTO stock_portofolio (users_id, stock, shares, price) VALUES (?, ?, ?, ?)",
                   session["user_id"], stock_symbol, sold_shares, stock_price)

        flash(
            f"You have just sold {symbol} stock, {shares} shares for {usd(transaction_profit)}")
        return redirect("/")

    else:
        # Select stock symbol from db stock_portofolio
        stock_symbol = db.execute("SELECT stock AS symbol " +
                                  "  FROM stock_portofolio WHERE users_id = ? " +
                                  " GROUP BY symbol",
                                  session["user_id"]
                                  )

        return render_template("sell.html", stock_symbol=stock_symbol)


@app.route("/add", methods=["GET", "POST"])
@login_required
def add():
    """Add additional cash to user accoun"""
    if request.method == "POST":
        # Post number of shares
        add_cash = int(request.form.get("cash").strip())
        # Check if input is not a positive integer
        # Ref. https://www.w3schools.com/python/ref_func_isinstance.asp
        if not add_cash or add_cash <= 0:
            return apology(f'"{add_cash}", must be positive intager', 400)

        # Update DB users table with addedcash
        db.execute("UPDATE users SET cash = cash + ? WHERE id = ?",
                   int(add_cash), session["user_id"])

        flash(
            f"You have just added {usd(add_cash)} to your account.")
        return redirect("/")

    else:
        return render_template("add.html")

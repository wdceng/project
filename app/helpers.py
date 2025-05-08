from flask import redirect, request, session, url_for
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            # Retrieve the current theme from the request arguments
            theme = request.args.get("t", "light")
            # Redirect to the login page with the theme parameter
            return redirect(url_for("login", t=theme))
        return f(*args, **kwargs)

    return decorated_function

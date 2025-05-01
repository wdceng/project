from flask import redirect, request, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            # Set default theme
            theme = request.args.get("t", "light")
            if theme not in ["dark", "light"]:
                theme = "light"
            return redirect(f"/login?t={theme}")
        return f(*args, **kwargs)

    return decorated_function

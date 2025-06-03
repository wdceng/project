from flask import redirect, url_for, request, session
from functools import wraps


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/latest/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect_with_theme("login")
        return f(*args, **kwargs)

    return decorated_function


# Redirect to the given view, keeping the theme ('t') parameter if present.
def redirect_with_theme(redirect_to):
    # Only pass the 't' parameter if it's in the request
    if "t" in request.args:
        # Retrieve the current theme from the request arguments
        # Redirect to the login page with the theme parameter
        return redirect(url_for(redirect_to, t=request.args.get("t")))
    else:
        return redirect(url_for(redirect_to))

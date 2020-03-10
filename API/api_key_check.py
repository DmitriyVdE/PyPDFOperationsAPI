from functools import wraps
from flask import request, abort
from flask_config import app

# The actual decorator function
def require_apikey(view_function):
  @wraps(view_function)
  # the new, post-decoration function. Note *args and **kwargs here.
  def decorated_function(*args, **kwargs):
    if request.args.get('key') and request.args.get('key') == app.secret_key:
      return view_function(*args, **kwargs)
    else:
      abort(401)
  return decorated_function
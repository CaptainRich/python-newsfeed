from flask import session, redirect
from functools import wraps


#####################################################################################################
def login_required(func):      # The 'login_required' function expects another function as an argument
  @wraps(func)
  def wrapped_function(*args, **kwargs):           # The new function returned by the decorator
    # if logged in, call original function with original arguments
    if session.get('loggedIn') == True:
      return func(*args, **kwargs)
      
    return redirect('/login')
  
  return wrapped_function
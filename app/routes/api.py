# Define the API endpoints for the application

from flask import Blueprint, request, jsonify, session
from app.models import User
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

@bp.route('/users', methods=['POST'])   #this route resolves to "/api/users"
def signup():
  data = request.get_json()
  db = get_db()

  try:
    # Attempt to create a new user
    newUser = User(
      username = data['username'],
      email = data['email'],
      password = data['password']
    )

    # save in database
    db.add(newUser)
    db.commit()
  except AssertionError:
    # Insert to database failed, send error to the front end
    # "Assert" errors are thrown when our custom validations fail.
    print(sys.exc_info()[0])
    print('Validation error')

    db.rollback()         #dump any failed/pending database connections
    return jsonify(message = 'Sign-up failed'), 500

  except sqlalchemy.exc.IntegrityError:
    # Insert to database failed, send error to the front end
    # "Integrity" errors are thrown when something specific to MySQL fails.
    print(sys.exc_info()[0])
    print('MySQL error')

    db.rollback()         #dump any failed/pending database connections
    return jsonify(message = 'Sign-up failed'), 500


  # Save the user's session information, so the application knows we're logged in.
  session.clear()                  #clear any previous session data first
  session['user_id'] = newUser.id
  session['loggedIn'] = True

  return jsonify(id = newUser.id)
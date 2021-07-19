# Define the API endpoints for the application

from app.utils.auth import login_required
from flask import Blueprint, request, jsonify, session
from app.models import User, Post, Comment, Vote
from app.db import get_db
import sys

bp = Blueprint('api', __name__, url_prefix='/api')

############################################################################################
# This is the route for a new user to 'sign-up'
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


############################################################################################
# This is the route for users to 'log-out'
@bp.route('/users/logout', methods=['POST'])
def logout():
  # remove session variables
  session.clear()
  return '', 204       #204 indicates 'no content'


############################################################################################
# This is the route for existing users to "log-in"
@bp.route('/users/login', methods=['POST'])
def login():
  data = request.get_json()
  db = get_db()

  try:
    user = db.query(User).filter(User.email == data['email']).one()
  except:
    print(sys.exc_info()[0])

  if user.verify_password(data['password']) == False:
    return jsonify(message = 'Incorrect credentials'), 400

  # If we get this far, assume all is ok and create the session
  session.clear()                  #clear any previous session data first
  session['user_id'] = user.id
  session['loggedIn'] = True

  return jsonify(id = user.id)

############################################################################################
# This is the route to create a new comment
@bp.route('/comments', methods=['POST'])
@login_required
def comment():
  data = request.get_json()
  db = get_db()

  try:
    # create a new comment
    newComment = Comment(
      comment_text = data['comment_text'],
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newComment)
    db.commit()

  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Comment failed'), 500

  return jsonify(id = newComment.id)            #on success, return the new comment ID


############################################################################################
# This is the route to add (increase) the vote for a post
@bp.route('/posts/upvote', methods=['PUT'])
@login_required
def upvote():
  data = request.get_json()
  db = get_db()

  try:
    # create a new vote with incoming id and session id
    newVote = Vote(
      post_id = data['post_id'],
      user_id = session.get('user_id')
    )

    db.add(newVote)
    db.commit()

  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Upvote failed'), 500

  return '', 204


############################################################################################
# This is the route to create a new post
@bp.route('/posts', methods=['POST'])
@login_required
def create():
  data = request.get_json()
  db = get_db()

  try:
    # create a new post
    newPost = Post(
      title = data['title'],
      post_url = data['post_url'],
      user_id = session.get('user_id')
    )

    db.add(newPost)
    db.commit()

  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post failed'), 500

  return jsonify(id = newPost.id)


############################################################################################
# This is the route to update/edit a post
@bp.route('/posts/<id>', methods=['PUT'])
@login_required
def update(id):
  data = request.get_json()       #"data" is a Python dictionary
  db = get_db()

  try:
    # Retrieve the post and update it (via the 'title' property)
    #SQLAlchemy requires a query of the database for the record, then modify the record
    # then recommit the record.
    post = db.query(Post).filter(Post.id == id).one()    #"post" is an object created from the "User" class
    post.title = data['title']
    db.commit()

  except:
    print(sys.exc_info()[0])
    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204


############################################################################################
# This is the route to delete a post
@bp.route('/posts/<id>', methods=['DELETE'])
@login_required
def delete(id):
  db = get_db()

  try:
    # Similar to an 'update', a 'delete post from db' requires a query first.
    db.delete(db.query(Post).filter(Post.id == id).one())
    db.commit()

  except:
    print(sys.exc_info()[0])

    db.rollback()
    return jsonify(message = 'Post not found'), 404

  return '', 204
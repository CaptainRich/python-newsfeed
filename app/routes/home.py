from flask import Blueprint, render_template, session, redirect      #import functions
from app.models import Post
from app.db import get_db

bp = Blueprint('home', __name__, url_prefix='/')  #consolidate routes into a single "bp" object

######################################################################################################################
@bp.route('/')                                    #route decorator to turn "index function" into a route
def index():
  # get all posts
  db = get_db()          #get a session connection tied to this route's context
  posts = db.query(Post).order_by(Post.created_at.desc()).all()   #get all the posts from this connection

  return render_template('homepage.html', 
                          posts=posts,
                          loggedIn=session.get('loggedIn')
                        )

######################################################################################################################
@bp.route('/login')                               #route decorator to turn "login function" into a route
def login():
  # IF not logged in yet
  if session.get('loggedIn') is None:
    return render_template('login.html')

  # Otherwise, redirect to the dashboard
  return redirect( '/dashboard' )

######################################################################################################################
@bp.route('/post/<id>')                           #route decorator to turn "single function" into a route
def single(id):
  # get single post by id
  db = get_db()
  post = db.query(Post).filter(Post.id == id).one()
  # render single post template
  return render_template(
    'single-post.html',
    post=post,
    loggedIn=session.get('loggedIn')
  ) 
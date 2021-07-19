from flask import Blueprint, render_template, session                     #import functions
from app.models import Post
from app.db import get_db
from app.utils.auth import login_required

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')   #consolidate routes into a single "bp" object

############################################################################################
@bp.route('/')
@login_required
def dash():

  db = get_db()
  posts = (
    db.query(Post)
    .filter(Post.user_id == session.get('user_id'))
    .order_by(Post.created_at.desc())
    .all()  )
     
  return render_template(
    'dashboard.html',                #route decorator to turn "dash function" into a route
    posts=posts,
    loggedIn=session.get('loggedIn') )

############################################################################################
@bp.route('/edit/<id>')
@login_required
def edit(id):

  # get single post by id
  db = get_db()
  post = db.query(Post).filter(Post.id == id).one()

  # render edit page
  return render_template(
    'edit-post.html',                     #route decorator to turn "edit function" into a route
    post=post,
    loggedIn=session.get('loggedIn')  )

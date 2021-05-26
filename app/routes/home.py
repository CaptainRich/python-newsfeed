from flask import Blueprint, render_template      #import functions

bp = Blueprint('home', __name__, url_prefix='/')  #consolidate routes into a single "bp" object

@bp.route('/')                                    #route decorator to turn "index function" into a route
def index():
  return render_template('homepage.html')

@bp.route('/login')                               #route decorator to turn "login function" into a route
def login():
  return render_template('login.html')

@bp.route('/post/<id>')                           #route decorator to turn "single function" into a route
def single(id):
  return render_template('single-post.html')  
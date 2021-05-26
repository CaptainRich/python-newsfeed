from flask import Blueprint, render_template                     #import functions

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')   #consolidate routes into a single "bp" object

@bp.route('/')
def dash():
  return render_template('dashboard.html')                       #route decorator to turn "dash function" into a route

@bp.route('/edit/<id>')
def edit(id):
  return render_template('edit-post.html')                       #route decorator to turn "edit function" into a route

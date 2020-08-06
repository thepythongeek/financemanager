
from flask import Blueprint 
from flask import render_template, request, url_for 



bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register')
def register():
    return render_template('register.html')
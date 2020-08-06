

from flask import Blueprint
from flask import render_template, url_for, redirect 



bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')
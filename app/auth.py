
import sqlalchemy
from flask import Blueprint 
from flask import render_template, request, url_for 
from flask import flash 
from flask import redirect
from flask_login import LoginManager
from flask_login import login_user
from app.models import db, User 


bp = Blueprint('auth', __name__, url_prefix='/auth')


# create an instance of LoginManager
login_manager = LoginManager()

#tell flask login how to load user from user id  
@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).get(user_id)  
    
    
@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        # get data from the form 
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # now check if we have a user with the given username 
        user = db.session.query(User).filter_by(username=name).one_or_none()
        if user:
            flash('user with username "{}" already exists'.format(user.username))
            return render_template('register.html')
        
        # if the user does not exist yet insert into database 
        # then redirect user to login 
        user = User(username=name, password=password, email=email)
        user.hash_password()
        db.session.add(user)
        try:
            db.session.commit()
        except sqlalchemy.exc.IntegrityError:
            flash('email already exists')
            return render_template('register.html')
        flash('Registration was a success')
        return redirect(url_for('.login'))
            
    return render_template('register.html')
    

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # obtain data from form 
        name = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # now do authentification 
        user = db.session.query(User).filter_by(username=name).one_or_none()
        if user is None:
            flash('User doesnot exist')
            return render_template('login.html')
        
        # if user is not none then the user is valid 
        # use the login_user function to log in the user 
        login_user(user)
        return redirect(url_for('main.index'))
    return render_template('login.html')
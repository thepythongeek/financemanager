
import datetime
import click
from werkzeug.security import generate_password_hash, check_password_hash
from flask.cli import AppGroup
from flask_sqlalchemy import SQLAlchemy 
from flask_login import UserMixin


# create an unbinded sqlachemy object 
db = SQLAlchemy()

# create a group to associate the database commands together 
db_cli = AppGroup('db')

# a command to generate all tables 
@db_cli.command('create-tables')
def create():
    db.create_all()
    click.echo('initialised database')
    
# a command line call to drop the database 
@db_cli.command('dropall')
def drop():
    db.drop_all()
    click.echo('Database dropped')

# now register this commands with the application 
def init_app(app):
    app.cli.add_command(db_cli)


# create the mappers
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(320), nullable=False, unique=True)
    password = db.Column(db.Text)
    
    #now create the relationships
    # a user can have many income as well expenses records 
    incomes = db.relationship('IncomeRecord', back_populates='user', lazy='dynamic')
    expenses = db.relationship('ExpensesRecord', back_populates='user', lazy='dynamic')
    
    def hash_password(self):
        self.password = generate_password_hash(self.password)
        
    def check_hashed_password(self, password):
        if check_password_hash(self.password, password):
            return True 
        else: return False 
    
    
    def __repr__(self):
        return '<User({})>'.format(self.username)
    
    

class IncomeRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(14), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    amount = db.Column(db.Float, nullable=False)
    
    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='incomes')
    
    def __repr__(self):
        return '<(Income({}, {})>'.format(self.item, self.date)
        
    
    def add(self):
        db.session.add(self)
        db.session.commit()

class ExpensesRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(14), nullable=False)
    date = db.Column(db.DateTime, default=datetime.datetime.now)
    amount = db.Column(db.Float, nullable=False)
    
    user_id = db.Column(db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='expenses')
    
    def __repr__(self):
        return '<Income({}, {})>'.format(self.item, self.date)
    
    def add(self):
        db.session.add(self)
        db.session.commit()
  
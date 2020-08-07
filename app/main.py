

from flask import Blueprint
from flask import render_template, url_for, redirect 
from flask import request
from flask import flash  
from flask_login import login_required
from flask_login import current_user
from app.models import IncomeRecord, ExpensesRecord, db, Inquiry



bp = Blueprint('main', __name__)


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    if request.method == 'POST':
        item = request.form.get('item')
        amount = request.form.get('amount')
        transaction = request.form.get('transaction')
        
        # depending on transaction type 
        # insert records to database 
        if transaction == 'expenses':
            record  = ExpensesRecord(item=item, amount=amount)
        else:
            record = IncomeRecord(item=item, amount=amount)
        record.user = current_user
        db.session.add(record)
        db.session.commit()
        flash('Your record has been stored successfully')
        
    # do calculations to get total expenses and net income for 
    # currently logged in user 
    expenses = (expenses.amount for expenses in current_user.expenses)
    incomes = (income.amount for income in current_user.incomes)
    total_expenses = sum(expenses)
    total_income = sum(incomes)
    net_income = total_income - total_expenses
    return render_template('index.html', income=net_income, expenses=total_expenses)
    

@bp.route('/Expenses')
@login_required
def expenses():
    return render_template('expenses.html')
    
    
@bp.route('/Income')
@login_required
def income():
    return render_template('income.html')
    

@bp.route('/inquiries', methods=['POST'])
@login_required
def inquiries():
    if request.method == 'POST':
        inquiries = request.form.get('inquiries')
        # insert the inquiry into database 
        inquiry = Inquiry(msg=inquiries)
        inquiry.author = current_user
        db.session.add(inquiry)
        db.session.commit()
        flash('Thank you we have recieved your inquiry')
        return redirect(url_for('main.index'))
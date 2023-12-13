from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from models import User
from flask_login import login_user, login_required, logout_user, current_user
from counter import Counter

assignUserId = Counter(0)

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    
    m = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('pwd')

    user = User.query.filter_by(email=m).first() # if this returns a user, then the email already exists in database

    if user:
        flash('email already exists')
        return redirect(url_for('auth.signup'))

    # TODO hash password for deployment
    new = User(assignUserId.get(), fname = name, email = m, pwd = password)

    assignUserId.increment()

    # add the new user to the database
    db.session.add(new)
    db.session.commit()

    return redirect(url_for('auth.login'))

@auth.route('/login', methods=['POST'])
def login_post():
    
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(email = email).first() #get email

    if user.password != password or not user:
        flash('wrong')
        return redirect(url_for('auth.login'))

    login_user(user, remember)
    return redirect(url_for('main.home'))

@auth.route('/profile')
@login_required
def profile():

    #lookup for current user is done through jinja current_user
    return render_template('profile.html')

@auth.route('/profile', methods=['POST'])
@login_required
def editProfile():

    check = current_user.get_id()

    user = User.query.filter_by(id = check).first_or_404()

    firstName = request.form.get('fName')
    lastName = request.form.get('lName')
    phoneNo = request.form.get('phoneNo')
    password = request.form.get('pwd')
    verify = request.form.get('verifyPwd')

    if password != verify:
        flash('Passwords do not match')
        return redirect(url_for('auth.profile'))

    user.firstName = firstName
    user.lastName = lastName
    user.phone_no = phoneNo
    user.password = password
    db.session.commit()         #save new changes

    return render_template('profile.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
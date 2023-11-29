from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from models import User

global counter
counter = 0

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/signup')
def signup():
    return render_template('signup.html')

@auth.route('/logout')
def logout():
    return render_template('logout.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    
    m = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=m).first() # if this returns a user, then the email already exists in database

    if user:
        flash('email already exists')
        return redirect(url_for('auth.signup'))

    # TODO hash password for deployment
    new = User(name, m, password)

    # add the new user to the database
    db.session.add(new)
    db.session.commit()

    return redirect(url_for('auth.login'))

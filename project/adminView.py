from counter import Counter
from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from models import Suggestion, User, Download, Schedule, Review, Attraction
from flask_login import login_user, login_required, logout_user, current_user

#TODO split up code into multiple files

assignId = Counter(0)

adminView = Blueprint('adminView', __name__)

def adminCheck():

    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return render_template('index.html')
    
    return

@adminView.route('/admin')
def admin():
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))

    return render_template('admin/home.html')

@adminView.route('/admin/users')
def adminUsers():
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))
    

    users = User.query.order_by(User.id).all()

    return render_template('admin/users.html', users = users)

@adminView.route('/admin/<int:userId>/downloads')
def adminViewDownloads(userId):
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))

    user = User.query.filter_by(id = userId).first()

    downloads = Download.query.filter_by(userId = user.id).all()
    schedules = []

    for x in downloads:
        schedule = Schedule.query.filter_by(scheduleId = x.scheduleId).first() 

        if schedule:
            schedules.append(schedule)

    return render_template('admin/userdownloads.html', user = user, schedules = schedules)

@adminView.route('/admin/<int:userId>/reviews')
def adminViewReviews(userId):
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))

    user = User.query.filter_by(id = userId).first()

    reviews = Review.query.filter_by(creatorId = user.id).all()

    return render_template('adminUserReviews.html', user = user, reviews = reviews)
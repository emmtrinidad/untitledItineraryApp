from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from models import User, Download, Schedule, Review
from flask_login import login_user, login_required, logout_user, current_user

#TODO perms


adminView = Blueprint('adminView', __name__)

@adminView.route('/admin')
def admin():

    return render_template('admin.html')

@adminView.route('/admin/users')
def adminUsers():

    users = User.query.order_by(User.id).all()

    return render_template('adminusers.html', users = users)

@adminView.route('/admin/<int:userId>/downloads')
def adminViewDownloads(userId):

    user = User.query.filter_by(id = userId).first()

    downloads = Download.query.filter_by(userId = user.id).all()
    schedules = []

    for x in downloads:
        schedule = Schedule.query.filter_by(scheduleId = x.scheduleId).first() 

        if schedule:
            schedules.append(schedule)

    return render_template('adminuserdownloads.html', user = user, schedules = schedules)

@adminView.route('/admin/<int:userId>/reviews')
def adminViewReviews(userId):

    user = User.query.filter_by(id = userId).first()

    reviews = Review.query.filter_by(creatorId = user.id).all()

    return render_template('adminUserReviews.html', user = user, reviews = reviews)
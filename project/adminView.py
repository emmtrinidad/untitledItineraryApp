from counter import Counter
from counter import Counter
from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from models import Suggestion, User, Download, Schedule, Review, Attraction
from flask_login import login_user, login_required, logout_user, current_user

#TODO split up code into multiple files

assignId = Counter(4)

adminView = Blueprint('adminView', __name__)

def adminCheck():

    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))
    
    return

@adminView.route('/admin')
def admin():
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))
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
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))

    user = User.query.filter_by(id = userId).first()

    reviews = Review.query.filter_by(creatorId = user.id).all()

    return render_template('admin/userreviews.html', user = user, reviews = reviews)

@adminView.route('/admin/<int:userId>/suggest')
def adminSuggestUser(userId):
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))

    user = User.query.filter_by(id = userId).first()

    if not user:
        render_template('admin/users.html')

    return render_template('admin/suggest.html', user = user)

@adminView.route('/admin/<int:userId>/suggest', methods = ['POST'])
def adminPostSuggestion(userId):
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))

    user = User.query.filter_by(id = userId).first()

    desc = request.form.get("description")

    if not user:
        redirect(url_for('adminView.admin'))

    new = Suggestion(id = assignId.get(), u = user.id, d = desc)
    assignId.increment()
    db.session.add(new)
    db.session.commit()
    

    return redirect(url_for('adminView.admin'))


@adminView.route('/admin/attractions/pending')
def adminViewPendingAttractions():
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))

    pending = Attraction.query.filter_by(approvedFlag = False).all()

    return render_template('admin/attractions.html', attractions = pending)

@adminView.route('/admin/attractions/<string:address>/approve')
def adminApproveAttraction(address):
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))

    toApprove = Attraction.query.filter_by(Address = address).first()
    toApprove.approvedFlag = True
    db.session.commit()

    return redirect(url_for('adminView.adminViewPendingAttractions'))

@adminView.route('/admin/attractions/<string:address>/remove')
def adminRemoveAttraction(address):
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))

    toDelete = Attraction.query.filter_by(Address = address).first()

    if not toDelete:
        return redirect(url_for('adminView.adminViewPendingAttractions'))


    db.session.delete(toDelete)
    db.session.commit()

    return redirect(url_for('adminView.adminViewPendingAttractions'))


@adminView.route('/admin/attractions')
def adminAttractions():
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))

    attractions = Attraction.query.order_by(Attraction.Address).all()

    return render_template('admin/attractions.html', attractions = attractions)

@adminView.route('/admin/suggestions')
def adminSuggestions():
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))

    suggestions = Suggestion.query.order_by(Suggestion.suggestionId).all()

    return render_template('admin/suggestions.html', suggestions = suggestions)

@adminView.route('/admin/reviews/pending')
def adminViewPendingReviews():
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))

    pending = Review.query.filter_by(approvedFlag = False).all()

    return render_template('admin/userreviews.html', reviews = pending)

@adminView.route('/admin/reviews/approve/<int:reviewId>')
def adminViewApproveReview(reviewId):
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))


    toApprove = Review.query.filter_by(reviewId = reviewId).first()

    toApprove.approvedFlag = True
    db.session.commit()

    return redirect(url_for('adminView.adminViewPendingReviews'))

@adminView.route('/admin/reviews/delete/<int:reviewId>')
@login_required
def adminViewDeleteReview(reviewId):
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()
    toDelete = Review.query.filter_by(reviewId = reviewId).first()


    if not toDelete.creatorId == check or not user.isAdmin:
        return redirect(url_for('main.index'))


    if not toDelete:
        return redirect(url_for('main.index'))

    db.session.delete(toDelete)
    db.session.commit()

    return redirect(url_for('adminView.adminViewPendingReviews'))

@adminView.route('/admin/<int:userId>/reviews')
@login_required
def adminViewUserReviews(userId):
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))
  
    toCheck = User.query.filter_by(id = userId).first()
    if not toCheck:
        return redirect(url_for('adminView.admin'))
    
    reviews = Review.query.filter_by(userId = userId).all()
    
    return render_template('admin/userreviews.html', user = toCheck, reviews = reviews)

@adminView.route('/admin/<int:userId>/downloads')
def adminViewUserDownloads(userId):
    check = current_user.get_id()
    user = User.query.filter_by(id = check).first()

    if not user or not user.isAdmin:
        return redirect(url_for('main.index'))
  
    toCheck = User.query.filter_by(id = userId).first()
    if not toCheck:
        return redirect(url_for('adminView.admin'))
    
    downloads = Download.query.filter_by(userId = userId).all()
    return render_template('userdownloads.html', user = toCheck)



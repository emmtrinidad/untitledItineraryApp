from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app import db
from models import Country, City, Province, Attraction, Review, User
import datetime
from counter import Counter

reviews = Blueprint('reviews', __name__)

idAssign = Counter(8)

@reviews.route('/locations/<string:cityCode>/<string:address>')
def seeReviews(cityCode, address):

    city = City.query.filter_by(airportCode = cityCode).first()
    attraction = Attraction.query.filter_by(Address = address).first()
    reviews = Review.query.filter_by(attractionAddress = address, approvedFlag = True).all()

    return render_template('review/reviews.html', city = city, attraction = attraction, reviews = reviews)

@reviews.route('/locations/<string:cityCode>/<string:address>/addreview')
@login_required
def addNewReviews(cityCode, address):

    city = City.query.filter_by(airportCode = cityCode).first()
    attraction = Attraction.query.filter_by(Address = address).first()

    return render_template('review/createreview.html', city = city, attraction = attraction)

@reviews.route('/locations/<string:cityCode>/<string:address>/addreview', methods = ['POST'])
@login_required
def postNewReview(cityCode, address):
    city = City.query.filter_by(airportCode = cityCode).first()
    attraction = Attraction.query.filter_by(Address = address).first()

    id = current_user.get_id()
    comment = request.form.get('comment')
    stars = request.form.get('stars')

    new = Review(idAssign.get(), address, id, comment, stars)
    idAssign.increment()

    db.session.add(new)
    db.session.commit()

    reviews = Review.query.filter_by(attractionAddress = address, approvedFlag = True).all()

    return render_template('review/reviews.html', city = city, attraction = attraction, reviews = reviews)

@reviews.route('/myreviews')
@login_required
def myReviews():
    id = current_user.get_id()

    reviews = Review.query.filter_by(creatorId = id).all()

    return render_template('review/myreviews.html', reviews = reviews)

@reviews.route('/myreviews/<int:reviewId>')
@login_required
def editReviewPage(reviewId):
    uId = current_user.get_id()
    user = User.query.filter_by(id = uId).first()

    review = Review.query.filter_by(reviewId = reviewId).first()

    if not review or review.creatorId != uId or not user.isAdmin:
        redirect(url_for('main.index'))


    return render_template('review/createreview.html', review = review)


@reviews.route('/myreviews/<int:reviewId>', methods = ['POST'])
@login_required
def editReview(reviewId):
    uId = current_user.get_id()
    user = User.query.filter_by(id = uId).first()

    review = Review.query.filter_by(reviewId = reviewId).first()

    if not review or review.creatorId != uId or not user.isAdmin:
        redirect(url_for('main.index'))

    comment = request.form.get('comment')
    stars = request.form.get('stars')

    review.comment = comment
    review.stars = stars
    review.approvedFlag = False     #upon editing, admin must recheck

    db.session.commit()

    reviews = Review.query.filter_by(creatorId = uId).all()

    return render_template('review/myreviews.html', reviews = reviews)

@reviews.route('/myreviews/<int:reviewId>/delete')
def deleteReview(reviewId):

    uId = current_user.get_id()
    user = User.query.filter_by(id = uId).first()

    review = Review.query.filter_by(reviewId = reviewId).first()

    if not review or review.creatorId != uId or not user.isAdmin:
        redirect(url_for('main.index'))

    db.session.delete(review)
    db.session.commit()

    return redirect(url_for('reviews.myReviews'))


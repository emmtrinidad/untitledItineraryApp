from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user
from app import db
from models import Country, City, Province, Attraction, Review
import datetime
from counter import Counter

reviews = Blueprint('reviews', __name__)

idAssign = Counter(0)

@reviews.route('/locations/<string:cityCode>/<string:address>')
def seeReviews(cityCode, address):

    city = City.query.filter_by(airportCode = cityCode).first()
    attraction = Attraction.query.filter_by(Address = address).first()
    reviews = Review.query.filter_by(attractionAddress = address, approvedFlag = True).all()

    return render_template('review/reviews.html', city = city, attraction = attraction, reviews = reviews)

@reviews.route('/locations/<string:cityCode>/<string:address>/addreview')
def addNewReviews(cityCode, address):

    city = City.query.filter_by(airportCode = cityCode).first()
    attraction = Attraction.query.filter_by(Address = address).first()

    return render_template('review/createreview.html', city = city, attraction = attraction)

@reviews.route('/locations/<string:cityCode>/<string:address>/addreview', methods = ['POST'])
def postNewReview(cityCode, address):
    city = City.query.filter_by(airportCode = cityCode).first()
    attraction = Attraction.query.filter_by(Address = address).first()

    id = current_user.get_Id()
    comment = request.form.get('comment')
    stars = request.form.get('stars')

    new = Review(idAssign.get(), address, id, comment, stars)
    idAssign.increment()

    db.session.add(new)
    db.session.commit()

    return render_template('review/reviews.html', city = city, attraction = attraction, reviews = reviews)



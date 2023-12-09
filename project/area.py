from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from models import Country, City, Province, Attraction
import datetime


area = Blueprint('area', __name__)

@area.route('/locations')
def locations():
    return 'placeholder for locations'

@area.route('/locations/countries')
def countries():

    countries = Country.query.order_by(Country.countryName).all()

    return render_template('countries.html', countries = countries)

@area.route('/locations/countries/<string:countryName>')
def country(countryName):

    country = Country.query.filter_by(countryName = countryName).first()

    if not country:
        return 'no countries but it works'
    
    return 'works'

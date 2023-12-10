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

@area.route("/locations/countries/<string:countryName>/provinces")
def provinces(countryName):
    country(countryName)

    provinces = Country.query.order_by(Country.provinces)
    return render_template("provinces.html", provinces=provinces)

# @area.route("/locations/countries/<string:countryName>/provinces/<string:provinceCode>")
# def province(countryName, provinceCode):
#     provinces(countryName)
    
#     province = Province.query.filter_by(provinceCode=provinceCode).first()

#     if not province:
#         return "province does not exist in database"
    
#     return render_template("province.html", province=province)

# @area.route("/locations/countries/<string:countryName>/provinces/<string:provinceCode>/cities")
# def cities(countryName, provinceCode):
#     province(countryName, provinceCode)
#     return "placeholder"

# @area.route("/locations/countries/<string:countryName>/provinces/<string:provinceCode>/cities/<string:name>")
# def city(countryName, provinceCode, name):
#     cities(countryName, provinceCode)
#     return "placeholder"

def countryQueryData(countryName):
    country = Country.query.filter_by(countryName = countryName).first()

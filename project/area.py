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

    country = countryQueryData(countryName)

    if not country:
        return 'no countries but it works'
    
    return 'works'

@area.route("/locations/<string:countryName>/provinces")
def provinces(countryName):
    countryQueryData(countryName)

    provinces = Province.query.order_by(Province.provinceCode).all()
    return render_template("provinces.html", provinces=provinces)

@area.route("/locations/<string:countryName>/provinces/<string:provinceCode>")
def province(countryName, provinceCode):
    countryQueryData(countryName)
    
    province = provinceQueryData(provinceCode)

    if not province:
        return "province does not exist in database"
    
    return render_template("province.html", province=province)

@area.route("/locations/<string:countryName>/<string:provinceCode>/cities")
def cities(countryName, provinceCode):
    countryQueryData(countryName)
    provinceQueryData(provinceCode)

    cities = City.query.order_by(City.name).all()
    return render_template("cities.html", cities=cities)

@area.route("/locations/<string:countryName>/<string:provinceCode>/cities/<string:name>")
def city(countryName, provinceCode, name):
    countryQueryData(countryName)
    provinceQueryData(provinceCode)
    city = cityQueryData(name)
    return render_template("city.html", city=city)

# Functions for retrieving data
def countryQueryData(countryName):
    return Country.query.filter_by(countryName = countryName).first()

def provinceQueryData(provinceCode):
    return Province.query.filter_by(provinceCode=provinceCode).first()

def cityQueryData(cityName):
    return City.query.filter_by(name=cityName).first()
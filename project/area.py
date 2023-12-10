from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import db
from models import Country, City, Province, Attraction
import datetime


area = Blueprint('area', __name__)

@area.route('/locations')
def locations():
    return render_template('area/locations.html')

@area.route('/locations/countries')
def countries():

    countries = Country.query.order_by(Country.countryName).all()

    return render_template('area/countries.html', countries = countries)

@area.route('/locations/countries/<string:countryName>')
def country(countryName):

    country = countryQueryData(countryName)

    if not country:
        return 'no countries but it works'  
    
    return render_template('area/country.html', country = country)

@area.route("/locations/<string:countryName>/provinces")
def provinces(countryName):
    countryQueryData(countryName)

    provinces = Province.query.order_by(Province.provinceName).all()
    return render_template("area/provinces.html", provinces=provinces)

@area.route("/locations/<string:countryName>/provinces/<string:provinceName>")
def province(countryName, provinceName):
    countryQueryData(countryName)
    
    province = provinceQueryData(provinceName)

    if not province:
        flash('province does not exist')
        return redirect(url_for('area.provinces(countryName)'))
    
    return render_template("area/province.html", province=province)

@area.route("/locations/<string:countryName>/<string:provinceName>/cities")
def cities(countryName, provinceName):
    countryQueryData(countryName)
    provinceQueryData(provinceName)

    cities = City.query.order_by(City.name).all()
    return render_template("area/cities.html", cities=cities)

@area.route("/locations/<string:countryName>/<string:provinceName>/cities/<string:cityCode>")
def city(countryName, provinceName, cityCode):
    countryQueryData(countryName)
    provinceQueryData(provinceName)
    city = cityQueryData(cityCode)
    attractions = Attraction.query.filter_by(cityCode = cityCode).all()

    return render_template("area/city.html", city=city, attractions = attractions)

@area.route("/locations/<string:cityCode>/addattraction")
def createAttraction(cityCode):

    city = cityQueryData(cityCode)

    if not city:
        flash('an error occurred')
        return redirect(url_for('area.locations'))

    return render_template("area/addattraction.html", city=city)

@area.route("/locations/<string:cityCode>/addattraction", methods = ['POST'])
def submitAttractionRequest(cityCode):

    city = cityQueryData(cityCode)
    province = provinceQueryData(city.provinceName)
    country = countryQueryData(city.countryName)

    name = request.form.get('attractionName')
    cost = request.form.get('cost')
    address = request.form.get('address')

    address = address.replace(" ", "") #remove all spaces

    rType = request.form.get('typeOfRestaurant')
    menu = request.form.get('menu')
    act = request.form.get('activity')

    if (menu and not rType) or (rType and not menu):
        flash('fill in both required elements for a restaurant')
        return render_template("area/addattraction.html", city=city)
    
    if any(not x.isalnum() for x in address):
        flash('do not add special characters to the address')
        return render_template("area/addattraction.html", city=city)
    

    new = Attraction(cc = cityCode, addy = address, name = name, cost = cost, restaurantType = rType, menu = menu, act = act)
    db.session.add(new)
    db.session.commit()

    attractions = Attraction.query.filter_by(cityCode = cityCode).all()

    return render_template("area/city.html", city=city, attractions = attractions)

@area.route("/search", methods = ['POST'])
def search():

    text = request.form.get('search')

    if not text:
        flash('please enter text')
        redirect(url_for('area.countries'))

    possibleCities = City.query.filter(City.name.contains(text)).all()
    possibleProvinces = Province.query.filter(Province.provinceName.contains(text)).all()
    possibleCountries = Country.query.filter(Country.countryName.contains(text)).all()

    return render_template('area/searchresults.html', countries = possibleCountries, provinces = possibleProvinces, cities = possibleCities)

# Functions for retrieving data
def countryQueryData(countryName):
    return Country.query.filter_by(countryName = countryName).first()

def provinceQueryData(provinceName):
    return Province.query.filter_by(provinceName=provinceName).first()

def cityQueryData(cityCode):
    return City.query.filter_by(airportCode = cityCode).first()

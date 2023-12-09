from datetime import datetime
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from app import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(64), nullable = False)
    lastName = db.Column(db.String(64), nullable = True)
    phone_no = db.Column(db.Integer, nullable = True)
    email = db.Column(db.String(320), unique = True, nullable = False)
    isAdmin = db.Column(db.Boolean, nullable=False)
    password = db.Column(db.String(100), nullable = False) # TODO implement hash for password once everything is good

    def __init__(self, fname, lname, email, phoneNo, pwd):
        self.firstName = fname
        self.lastName = lname
        self.email = email
        self.isAdmin = False
        self.phone_no = phoneNo 
        self.password = pwd

    def __init__(self, fname, email, pwd):
        self.firstName = fname
        self.email = email
        self.password = pwd

        self.isAdmin = False


    reviews = db.relationship('Review', backref='user', lazy = True)
    schedules = db.relationship('Schedule', backref='user', lazy = True)
    events = db.relationship('Event', backref = 'user', lazy = True)

class Schedule(db.Model):
    creatorId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    scheduleId = db.Column(db.Integer, primary_key = True)
    scheduleName = db.Column(db.String(300), nullable = False)
    startDate = db.Column(db.DateTime, nullable = False)
    endDate = db.Column(db.DateTime, nullable = False)

    def __init__(self,cId, sId, name, startD, endD):
        self.creatorId = cId
        self.scheduleId = sId
        self.scheduleName = name
        self.startDate = startD
        self.endDate = endD

class Event(db.Model):
    eventId = db.Column(db.Integer, primary_key = True)
    creatorId = db.Column(db.Integer, db.ForeignKey('user.id'))
    scheduleId = db.Column(db.Integer, db.ForeignKey('schedule.scheduleId'))
    startTime = db.Column(db.DateTime, nullable = False)
    endTime = db.Column(db.DateTime, nullable = False)
    location = db.Column(db.String(300), db.ForeignKey('attraction.Address'), nullable = True) #does not always need set location
    cityCode = db.Column(db.String(3), db.ForeignKey('city.airportCode'))

    def __init__(self, eId, cId, sId, startTime, endTime, location, city):
        self.eventId = eId
        self.creatorId = cId
        self.scheduleId = sId
        self.startTime = startTime
        self.endTime = endTime
        self.location = location
        self.cityCode = city

class Country(db.Model):
    countryName = db.Column(db.String, primary_key = True)
    officialLanguage = db.Column(db.String(100), nullable = False)
    provinces = db.relationship('Province', backref = 'country', lazy = True)
    cities = db.relationship('City', backref = 'country', lazy = True)

class Province(db.Model):
    provinceCode = db.Column(db.Integer, primary_key = True)
    countryName = db.Column(db.String(200), db.ForeignKey('country.countryName'), nullable = False)
    timezone = db.Column(db.String(3), nullable = False)
    climate = db.Column(db.String(200), nullable = False)
    cities = db.relationship('City', backref = 'province', lazy = True)

class City(db.Model):
    airportCode = db.Column(db.String(3), primary_key = True)
    name = db.Column(db.String(200), nullable = False)
    provinceCode = db.Column(db.Integer, db.ForeignKey('province.provinceCode'))
    countryName = db.Column(db.Integer, db.ForeignKey('country.countryName'))
    attractions = db.relationship('Attraction', backref = 'attraction', lazy = True)

class Review(db.Model):
    creatorId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    comment = db.Column(db.String(3000), nullable = True) #people can just leave only starred reviews
    stars = db.Column(db.Integer, nullable = False)
    approvedFlag = db.Column(db.Boolean, nullable = False)

class Suggestion(db.Model):

    userId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    adminId = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key = True)
    user = db.relationship("User", foreign_keys=[userId])
    admin = db.relationship("User", foreign_keys=[adminId])
    description = db.Column(db.String(3000), nullable = False) # review is nothing without the description

class Attraction(db.Model):
    cityCode = db.Column(db.String, db.ForeignKey('city.airportCode'), nullable = False)
    Address = db.Column(db.String(300), primary_key  =True)
    Name = db.Column(db.String(200), nullable = False)
    Cost = db.Column(db.Integer, nullable = False) #rank from 0-3 in terms of free to expensive

    typeOfRestaurant = db.Column(db.String(), nullable = True)
    menu = db.Column(db.String(), nullable = True) #href to link for menu
    activity = db.Column(db.String(50), nullable = False)
    approvedFlag = db.Column(db.Boolean, nullable = False)

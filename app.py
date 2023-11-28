from datetime import datetime
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
#TODO put everything in different files

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) #nullable allows for non-empty values
    completed = db.Column(db.Integer, default = 0) #never used
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<task %r>' % self.id    #when created will return task and its id
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(64), nullable = False)
    lastName = db.Column(db.String(64), nullable = False)
    phone_no = db.Column(db.Integer, nullable = True)
    email = db.Column(db.String(320), unique = True, nullable = False)
    isAdmin = db.Column(db.Boolean, nullable=False)

    def __init__(self, fname, lname, email, phoneNo):
        self.firstName = fname
        self.lastName = lname
        self.email = email
        self.isAdmin = False
        self.phone_no = phoneNo 

    password = db.Column(db.String(100), nullable = False) # TODO implement hash for password once everything is good

    reviews = db.relationship('Review', backref='user', lazy = True)
    schedules = db.relationship('Schedule', backref='user', lazy = True)
    events = db.relationship('Event', backref = 'user', lazy = True)

class Schedule(db.Model):
    creatorId = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    scheduleId = db.Column(db.Integer, primary_key = True)
    startDate = db.Column(db.DateTime, nullable = False)
    endDate = db.Column(db.DateTime, nullable = False)

class Event(db.Model):
    creatorId = db.Column(db.Integer, db.ForeignKey('user.id'))
    scheduleId = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date, nullable = False)
    startTime = db.Column(db.DateTime, nullable = False)
    endTime = db.Column(db.DateTime, nullable = False)

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



@app.route('/') #url string of app here
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
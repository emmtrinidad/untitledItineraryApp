from datetime import datetime
from flask import Flask, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.app_context().push()

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False) #nullable allows for non-empty values
    completed = db.Column(db.Integer, default = 0) #never used
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<task %r>' % self.id    #when created will return task and its id
    
class User(db.model):
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(64), nullable = False)
    lastName = db.Column(db.String(64), nullable = False)
    phone_no = db.Column(db.Integer(10), nullable = True)
    email = db.Column(db.String(320), nullable = False)
    isAdmin = db.Colum(db.Boolean, nullable=False)
     
    name = composite(Point, firstName, lastName)


@app.route('/') #url string of app here
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
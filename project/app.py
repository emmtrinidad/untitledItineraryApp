from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# init SQLAlchemy so we can use it later in our models
db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = '\xa5\xeeZy(\x9e\x169Wo\xf4\xc0'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'

db.init_app(app)


# blueprint for auth routes in our app
from auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint)

# blueprint for non-auth parts of app
from main import main as main_blueprint
app.register_blueprint(main_blueprint)

from sched import sched as sched_blueprint
app.register_blueprint(sched_blueprint)

from adminView import adminView as adminView_blueprint
app.register_blueprint(adminView_blueprint)
from area import area as area_blueprint
app.register_blueprint(area_blueprint)

from reviews import reviews as reviews_blueprint
app.register_blueprint(reviews_blueprint)

from area import area as area_blueprint
app.register_blueprint(area_blueprint)

app.app_context().push()
db.create_all()

lm = LoginManager()
lm.login_view = 'auth.login'
lm.init_app(app)

from models import User
@lm.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

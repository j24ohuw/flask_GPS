from flask import Flask
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

from instance.config import app_config
# local imports
db = SQLAlchemy()
app = Flask(__name__)
# from app import routes

def create_app(config_name):
    from .models import Location, TimeSeries
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    return app

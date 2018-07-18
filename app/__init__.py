from flask import jsonify, request, make_response
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema, fields, ValidationError, pre_load
# local imports
from instance.config import app_config
from sqlalchemy.exc import IntegrityError

# init database
db = SQLAlchemy()


## id	description	datetime	longitude	latitude	elevation
def create_app(config_name):
    from .models import Location, TimeSeries, LocationSchema, TimeSeriesSchema
    location_schema, timeseries_schema = LocationSchema(), TimeSeriesSchema()
    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    session = db.session

    @app.route('/')
    @app.route('/index')
    def index():
        return "Hello, World!"

    # routing function for ListCreateAPIView
    @app.route('/locations/', methods=['POST'])
    def locations():
        # json_input = request.get_json()
        json_input = request.data
        # empty data, return error code 400
        if not json_input:
            return jsonify({'message': 'No input provided'}), 400
        try:
            data = location_schema.load(data=json_input, session=session)
        except ValidationError as err:
            return jsonify(err.messages), 422
        # if location does not exist, add new location
        location = Location.query.filter_by(description=json_input['description']).first()
        if location is None:
            # create a new location
            description = request.data['description']
            location = Location(description=description)
            message = "New location created"
            db.session.add(location)
            db.session.commit()
        else:
            message = 'Added new datapoint to an existing location'

        # if post request is a duplicate
        """Implementation for duplicate prevention goes here"""

        # append new timeseries data to location
        timeseries = TimeSeries(datetime=request.data['datetime'],
                                longitude=request.data['longitude'],
                                latitude=request.data['latitude'],
                                elevation=request.data['elevation'],
                                location_id=location.id,
        )
        db.session.add(timeseries)
        db.session.commit()
        result = timeseries_schema.dump(TimeSeries.query.get(timeseries.id))
        return jsonify({
            'message': message,
            'result': result
        })




    return app




# app = Flask(__name__)
# from app import routes

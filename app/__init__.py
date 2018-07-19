from flask import jsonify, request, make_response, abort
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
    from .models import Product, Location, ProductSchema, LocationSchema
    product_schema = ProductSchema()
    products_schema = ProductSchema(many=True)
    location_schema = LocationSchema()
    locations_schema = LocationSchema(many=True)

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    @app.route('/')
    @app.route('/index')
    def index():
        return "Hello, World!"

    # routing function for ListCreateAPIView
    @app.route('/products/', methods=['POST'])
    def add_location():
        message = ''
        post_input = request.data
        # empty data, return error code 400
        if not post_input:
            return jsonify({'message': 'No input provided','error':400}), 400
        # validate data; deserialize
        try:
            data = product_schema.load(data=post_input, session=db.session)
        # raise validation error if deserialization fails
        except ValidationError as err:
            return jsonify(err.messages), 422

        # if the description does not exist, add a new description
        product = Product.query.filter_by(description=post_input['description']).first()
        if product is None:
            message = 'New product registered'
            # create a new location
            description = request.data['description']
            product = Product(description=description)
            db.session.add(product)
            db.session.commit()

        # if post request is a duplicate
        """Implementation for duplicate prevention goes here"""

        # append a new location datum to product
        location = Location(datetime=request.data['datetime'],
                                longitude=request.data['longitude'],
                                latitude=request.data['latitude'],
                                elevation=request.data['elevation'],
                                product_id=product.id,
        )
        db.session.add(location)
        db.session.commit()
        result = location_schema.dump(Location.query.get(location.id))
        return jsonify({
            'message': message,
            'result': result
        })

    @app.route('/products/', methods=['GET'])
    def product_listview():
        products = Product.query.all()
        result = products_schema.dump(products)
        return jsonify({
            'result': result
        })

    @app.route('/products/<int:pk>', methods=['GET'])
    def location_detail(pk):
        product = Product.query.filter_by(id=pk).all()
        # detail can only retrieve single object
        assert len(Product) < 2
        # serialize
        result = products_schema.dump(product)
        return jsonify({'result':result})



    @app.route('/products/<int:pk>', methods=['DELETE'])
    def location_detail_delete(pk):
        product = Product.query.filter_by(id=pk).first()
        print(product)
        if not product:
            return make_response(jsonify({'message': 'No entry was found for the given id',
                                          'error':'404'})), 404
        else:
            try:
                db.session.delete(product)
                db.session.commit()
                return make_response(jsonify({'message':'location entry was successfully deleted'})), 201
            except:
                return make_response(jsonify({'message': 'location entry deletion was unsuccessful',
                                              'error':'400'})), 400

    # @app.route('/locations/<>')
    return app


# app = Flask(__name__)
# from app import routes


# else:
#     Location.query.filter_by(datetime=request.data['datetime'],
#                               longitude=request.data['longitude'],
#                               latitude=request.data['latitude'],
#                               elevation=request.data['latitude'],
#                               product_id=product.id
#     )
#     message = 'Added a new datapoint to an existing location'

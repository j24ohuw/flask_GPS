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

    # routing function for ListCreateAPIView
    @app.route('/products/', methods=['POST'])
    def add_product():
        message = ''
        post_input = request.data
        # verify if passed time input is of ISO format
        try:
            time = Location.validate_time(request.data['datetime'])
        except ValidationError as err:
            return jsonify({'error': str(err)}), 400
        # empty data, return error code 400
        if not post_input:
            return jsonify({'error': 'No input provided'}), 400

        # validate data; deserialize
        try:
            data = product_schema.load(data=post_input, session=db.session)
        # raise validation error if deserialization fails
        except ValidationError as err:
            return jsonify(str(err)), 422

        # Always create a new product
        description = request.data['description']
        product = Product(description=description)
        product.save()
        # append a new location datum to product
        location = Location(datetime=time,
                                longitude=request.data['longitude'],
                                latitude=request.data['latitude'],
                                elevation=request.data['elevation'],
                                product_id=product.id,
        )
        try:
            location.save()
        except ValidationError as err:
            return jsonify({'error': str(err)}), 422

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

    @app.route('/products/<int:pk>', methods=['GET', 'PUT'])
    def location_detail(pk):

        product = Product.query.filter_by(id=pk).first()
        # check empty data
        if not product:
            return make_response(jsonify({'message': 'No entry was found for the given id',
                                          'error':'404'})), 404

        if request.method == 'GET':
            # serialize
            result = product_schema.dump(product)
            return jsonify({'result':result})
        # process PUT request
        else:
            product.description = request.data['description']
            try:
                product.save()
                return make_response(
                    jsonify({'message': 'product editing was successful',
                             'result': product_schema.dump(product)}), 200
                )
            except ValidationError as e:
                return make_response(
                    jsonify({'error': e}), 422
                )




    @app.route('/products/<int:pk>', methods=['DELETE'])
    def location_detail_delete(pk):
        product = Product.query.filter_by(id=pk).first()
        if not product:
            return make_response(jsonify({'message': 'No entry was found for the given id',
                                          'error':'404'})), 404
        else:
            try:
                # db.session.delete(product)
                # db.session.commit()
                product.delete()
                return make_response(jsonify({'message':'location entry was successfully deleted'})), 201
            except Exception as e:
                return make_response(jsonify({'error':e})), 400

    # adds location data to a product; time, longitude, latitude, and elevation must be given
    # product ID must be given as URL
    @app.route('/products/<int:product_pk>', methods=['POST'])
    def location_post(product_pk):
        product = Product.query.filter_by(id=product_pk).first()
        if not product:
            return make_response(jsonify({'error': 'No entry was found for the given id'})), 404
        # product exists
        else:
            try:
                time = Location.validate_time(request.data['datetime'])
            except ValidationError as err:
                make_response(jsonify({'error': err})), 422

            # check for duplicate
            longitude = request.data['longitude']
            latitude = request.data['latitude']
            elevation = request.data['elevation']

            locations = Location.query.filter_by(product_id=product_pk)\
                .filter_by(longitude=longitude, latitude=latitude, elevation=elevation).all()
            print(locations)
            # duplicates -> return error
            if locations:
                return make_response(jsonify({'error': 'Duplicate entry exists'})), 404

            try:
                location = Location(datetime=time,
                                    longitude=longitude,
                                    latitude=latitude,
                                    elevation=elevation,
                                    product_id=product_pk
                                    )

                location.save()
                result = location_schema.dump(location)
                return make_response(
                    jsonify({
                        'message': 'new location added to a product',
                        'result': result,
                    })
                )
            except ValidationError as e:
                return make_response(jsonify({'error':e})), 422


    @app.route('/locations/<int:location_pk>', methods=['PUT', 'DELETE'])
    def location_edit(location_pk):
        # validate input data
        # check the nested relationship and see if the passed values make sense
        location = Location.query.filter_by(id=location_pk).first()
        # if location is empty return error message
        if not location:
            return make_response(jsonify({'message': 'No entry was found for the given id',
                                          'error': '404'})), 404

        if request.method == 'PUT':
            location.elevation = request.data.get('elevation','')
            location.longitude = request.data.get('longitude','')
            location.latitude = request.data.get('latitude','')
            location.datetime = request.data.get('datetime','')

            try:
                location.save()
                result = location_schema.dump(location)
                return make_response(
                    jsonify({'message': 'location edited',
                             'result': result
                             })), 200
            except ValidationError as err:
                return jsonify(err.messages), 422

        if request.method == 'DELETE':
            try:
                location.delete()
                return make_response(
                    jsonify({
                        'message': 'location deleted',
                     })), 200
            # if for some reason delete fails, we raise 400
            except:
                abort(400)

    return app

# data = {'datetime': request.data['datetime'],
#         'longitude': request.data['longitude'],
#         'latitude': request.data['latitude'],
#         'elevation': request.data['elevation']
# }
# try:
#     location_validate = location_schema.load(data=data, session=db.session)
# except ValidationError as err:
#     return jsonify(err.messages), 422

# # if post request is a duplicate;
# """Implementation for duplicate prevention goes here"""

# # if the description does not exist, add a new description
# product = Product.query.filter_by(description=post_input['description']).first()
# if product is None:
#     message = 'New product registered'
#     # create a new location
#     description = request.data['description']
#     product = Product(description=description)
#     db.session.add(product)
#     db.session.commit()
#
# # if post request is a duplicate
# """Implementation for duplicate prevention goes here"""


# else:
#     Location.query.filter_by(datetime=request.data['datetime'],
#                               longitude=request.data['longitude'],
#                               latitude=request.data['latitude'],
#                               elevation=request.data['latitude'],
#                               product_id=product.id
#     )
#     message = 'Added a new datapoint to an existing location'




# app = Flask(__name__)
# from app import routes

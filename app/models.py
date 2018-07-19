# import database and marshmallow
from app import db
from marshmallow import Schema, fields, ValidationError, pre_load
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields, pre_dump, post_dump
from .utils import SmartNested

# data example:
# id	description	datetime	longitude	latitude	elevation
class Product(db.Model):
    """This class represents product model"""
    # __tablename__ = 'Product'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False, unique=True)
    locations = db.relationship('Location', backref='product',
                            order_by='Location.datetime',
                            cascade="all, delete-orphan",
                            lazy='dynamic'
    )

    def __init__(self, description):
        self.description = description

    def save(self):
        db.session.add(self)
        db.session.commit()

class Location(db.Model):
    # __tablename__ = 'Location'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey(Product.id), nullable=False) #foreignkey input takes tablename
    datetime = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Float, nullable=False)

    def __init__(self, product_id, datetime, longitude, latitude, elevation):
        self.product_id = product_id
        self.datetime = datetime
        self.longitude = longitude
        self.latitude = latitude
        self.elevation = elevation

    def save(self):
        """Save timeseries data.
        This applies for both creating a new one
        and updating an existing onupdate
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def get_all(location_id):
        """this method gets entire history for a given location"""
        # return Location.query.filter_by(id=location_id)
        return Location.query.all()

    def __repr__(self):
        """Return a representation of a location instance."""
        return "<Location: {}>".format(self.id)


class ProductSchema(ModelSchema):
    # overriding automatic history field from model import
    id = fields.Int(dump_only=True)

    @post_dump(pass_many=True)
    def wrap(self, data, many):
        if many:
            for product in data:
                history = []
                product_id = product['id']
                historical_locations = Location.query.filter_by(product_id=product_id)#.all()

                for location in historical_locations:
                    obj = {
                        'id': location.id,
                        'datetime': location.datetime,
                        'longitude':location.longitude,
                        'latitude': location.latitude,
                        'elevation': location.elevation,
                    }
                    history.append(obj)
                product['locations'] = history
        else:
            data = {'description':data['description'],
                     'id': data['id'],
             }
        return data

    class Meta:
        model = Product


    # historical_data = fields.Method('format_timeseries', dump_only=True)
    #
    # def format_timeseries(self, location):
    #     timeseries = location
    #     return '{},{}, {}, {}'.format(timeseries.datetime,
    #                                   timeseries.longitude,
    #                                   timeseries.latitude,
    #                                   timeseries.elevaton)
    # history = fields.Nested(HistorySchema, many=True)
    # class Meta:
    #     model = Location
class LocationSchema(ModelSchema):
    id = fields.Int(dump_only=True)
    location = fields.Nested(ProductSchema)
    class Meta:
        model = Location

    # method to invoke after deserialization. Takes deserialized data; Returns user-friendly processed data
    # @post_load

    # method to invoke before serializing an object; receives object returns processed object
    # @pre_dump

    # @post_dump
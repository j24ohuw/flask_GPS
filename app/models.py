# import database and marshmallow
from app import db
from marshmallow import Schema, fields, ValidationError, pre_load
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from .utils import SmartNested

# data example:
# id	description	datetime	longitude	latitude	elevation
class Location(db.Model):
    """This class represents location model"""
    # __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    history = db.relationship('TimeSeries', backref='location',
                            order_by='TimeSeries.datetime',
                            cascade="all, delete-orphan",
                            lazy='dynamic'
    )

    def __init__(self, description):
        self.description = description

    def save(self):
        db.session.add(self)
        db.session.commit()

class TimeSeries(db.Model):
    # __tablename__ = 'timeseries'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey(Location.id), nullable=False) #foreignkey input takes tablename
    datetime = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Float, nullable=False)

    def __init__(self, location_id, datetime, longitude, latitude, elevation):
        self.location_id = location_id
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
        """Return a representation of a timeseries instance."""
        return "<Timeseries: {}>".format(self.id)


# class TimeSeriesSchema(ma.ModelSchema):
#     id = fields.Int(dump_only=True)
#     location = fields.Nested(LocationSchema)
#
#     class Meta:
#         model = TimeSeries


class LocationSchema(ModelSchema):
    # overriding automatic history field from model import
    id = fields.Int(dump_only=True)
    # history = fields.Nested(HistorySchema, many=True)
    class Meta:
        model = Location

class TimeSeriesSchema(ModelSchema):
    id = fields.Int(dump_only=True)
    location = fields.Nested(LocationSchema)
    class Meta:
        model = TimeSeries

    # method to invoke after deserialization. Takes deserialized data; Returns user-friendly processed data
    # @post_load

    # method to invoke before serializing an object; receives object returns processed object
    # @pre_dump

    # @post_dump
from app import db


# data example:
# id	description	datetime	longitude	latitude	elevation
class Location(db.Model):
    """This class represents location model"""
    __tablename__ = 'locations'

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(255), nullable=False)
    history = db.relationship(
        'TimeSeries', backref='description', order_by='TimeSeries.id', cascade="all, delete-orphan"
    )

    def __init__(self, description):
        self.description = description

    def save(self):
        db.session.add(self)
        db.session.commit()


class TimeSeries(db.Model):
    __tablename__ = 'timeseries'

    id = db.Column(db.Integer, primary_key=True)
    location_id = db.Column(db.Integer, db.ForeignKey(Location.id))
    datetime = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    elevation = db.Column(db.Float, nullable=False)

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

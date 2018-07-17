import unittest
import os
import json
from app import db, create_app
from app.models import Location, TimeSeries

class TimeSeriesTestCase(unittest.TestCase):
    """This test class represents the model test cases for timeseires and location"""

    def setUp(self):
        """Define test variables and initialize the app"""
        self.app = create_app(config_name="testing")
        self.client = self.app.test_client
        self.location = {'description': 'Cesna 120'}
        self.history0 = {'datetime': '2016-10-12T12:00:00-05:00',
                         'longitude':'43.2583264',
                         'latitude': '43.2583264',
                         'elevation': '500'
        }

        self.history1 = {'datetime': '2016-10-13T12:00:00-05:00',
                         'longitude':'42.559112',
                         'latitude': '-79.286693',
                         'elevation': '550'
        }

        # bind the app to the current context
        with self.app.app_context():
            # create all tables
            # db.session.close()
            # db.drop_all()
            db.create_all()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def test_location_setup(self):
        """Test case for setting up database location model"""
        test_location = Location(**self.location)
        db.session.add(test_location)
        db.session.commit()

    def test_history_setup(self):
        """Test case for setting up database timeseries model"""
        location = Location(**self.location)
        test_history0 = TimeSeries(**self.history0, description=location)
        db.session.add(test_history0)
        db.session.commit()
        for key in self.location:
            self.assertIn(self.location[key], Location.query.filter_by(id=id).first())
        for key in self.history0:
            self.assertIn(self.history[key], Location.query.filter_by(id=id).first())

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()


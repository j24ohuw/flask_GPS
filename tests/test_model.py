# import unittest
# import os
# import json
# from app import db, create_app
# from app.models import Location, TimeSeries, LocationSchema, TimeSeriesSchema
# from sqlalchemy.exc import IntegrityError, DataError
# from marshmallow import ValidationError

# location_schema = LocationSchema()
# history_schema = TimeSeriesSchema()

# class TimeSeriesTestCase(unittest.TestCase):
#     """This test class represents the model test cases for timeseires and location"""

#     def setUp(self):
#         """Define test variables and initialize the app"""
#         self.app = create_app(config_name="testing")
#         self.client = self.app.test_client
#         self.location = {'description': 'Cesna 120'}
#         self.history0 = {'datetime': '2016-10-12T12:00:00-05:00',
#                          'longitude':'43.2583264',
#                          'latitude': '43.2583264',
#                          'elevation': '500'
#         }

#         self.history1 = {'datetime': '2016-10-13T12:00:00-05:00',
#                          'longitude':'42.559112',
#                          'latitude': '-79.286693',
#                          'elevation': '550'
#         }
#         # DC-6 Twin Otter	2016-10-12T12:00:00-05:00	43.459112	-80.386693	500
#         self.new_location = {'description': 'DC-6 Twin Otter',
#                              'datetime':'2016-10-12T12:00:00-05:00',
#                              'longitude': '43.459112',
#                              'latitude': '43.2583264',
#                              'elevation': '500'
#                              }

#         self.old_location = {}

#         # bind the app to the current context
#         with self.app.app_context():
#             # create all tables
#             db.session.close()
#             db.drop_all()
#             db.create_all()

#     def tearDown(self):
#         """teardown all initialized variables."""
#         with self.app.app_context():
#             # drop all tables
#             db.session.remove()
#             db.drop_all()

#     def test_location_setup(self):
#         """Test case for setting up database location model"""
#         test_location = Location(**self.location)
#         db.session.add(test_location)
#         db.session.commit()

#     def test_history_setup(self):
#         """Test case for setting up database timeseries model"""
#         location = Location(**self.location)
#         db.session.add(location)
#         db.session.commit()
#         history = TimeSeries(**self.history0, location_id=location.id)
#         db.session.add(history)
#         db.session.commit()
#         self.assertEqual(location.id, history.location_id)

#     def test_location_schema_serialization(self):
#         """Test case for default serialization"""
#         location = Location(**self.location)
#         # load the schema
#         db.session.add(location)
#         schema_result = location_schema.dump(location)
#         print(schema_result)
#         for key in self.location:
#             assert self.location[key] == schema_result.data[key]
#         try:
#             data = location_schema.load(data=json.dump(schema_result), session=db.session)
#             print(data)
#         except ValidationError:
#             raise ValidationError


#     def test_location_create(self):
#         """Testcase for baseic location create"""
#         # data = json.dumps(self.new_location)
#         result = self.client().post(
#             '/locations/',
#             data=self.new_location
#         )
#         self.assertEqual(result.status_code, 200)
#         self.assertIn(self.new_location['description'], str(result.data))

#     # def test_except_default_validation_error(self):
#     #     """Test for default validation error"""
#     #     location = self.location
#     #     # location length is limited to 255 by model;
#     #     # this test should also fail because the description is purely numbers
#     #     location['description'] = '100' * 100
#     #     result = self.client().post(
#     #         '/locations/',
#     #         data=self.location
#     #     )
#     #     self.assertEqual(DataError, result.status_code)

#     def test_duplicate_post(self):
#         """Duplicate objects should not be allowed"""
#         result = self.client().post(
#             '/locations/',
#             data=self.location
#         )
#         self.assertEqual(result, 201)
#         result = self.client().post(
#             '/locations/',
#             data=self.location
#         )
#         # duplicate is not allowed -> bad request
#         self.assertEqual(result, 400)


#     def test_location_update(self):
#         pass

#     def test_location_delete(self):
#         pass

#     def test_timeseries_create(self):
#         pass

#     def test_timeseries_update(self):
#         pass

#     def test_timeseries_delete(self):
#         pass

#     def test_timeseries_schema_serialization(self):
#         """Test case for default timeseries serialization"""
#         pass

#     def test_joint_schema_serialization(self):
#         """Testcase for serializing both schemas given
#             id	description	datetime	longitude	latitude	elevation """
#         pass

#     def test_wrong_datatype_serialization(self):
#         """Testcase for disallowing serialization of wrong data type"""
#         pass


# # Make the tests conveniently executable
# if __name__ == "__main__":
#     unittest.main()


import resource
import unittest
import json
from pymongo import MongoClient

db = None

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.app = resource.app.test_client()

        # Run app in testing mode to retrieve exceptions and stack traces
        resource.app.config['TESTING'] = True

        # Inject test database into application
        mongo = MongoClient('localhost', 27017)
        global db
        db = mongo.test_database
        resource.app.db = db

        ## We do this to clear our database before each test runs
        # db.drop_collection('users')

    def test_getting_a_user(self):

        pass
        # new_user = request.json
        # users_collection = app.db.users
        # result = users_collection.insert_one(new_user)
        # user = users_collection.find_one({"_id": result.inserted_id})
        # return user

        # ## Post 2 users to database
        # self.app.post('/users/', headers=None, data=json.dumps(dict(name="Eliel Gordon", email="eliel@example.com")), content_type='application/json')
        #
        # ## 3 Make a get request to fetch the posted user
        #
        # response = self.app.get('/users/', query_string=dict(name="goku"))
        #
        # # Decode reponse
        #
        # response_json = json.loads(response.data.decode())
        #
        #
        # ## Actual test to see if GET request was succesful
        # ## Here we check the status code
        # self.assertEqual(response.status_code, 200)

    def test_delete_user(self):
        # self.app.delete('/users/', query_string=dict(name="goku"))
        pass
        # user_name = request.args.get('name')
        # users_collection = app.db.users
        # users_collection.remove({'name': user_name})

        # self.assertEqual(response.status_code, 200)

    def test_patch_user(self):
        self.app.patch('/users/', query_string=dict(user="bob", new_user="spongebob"))

        response = self.app.get('/users/', query_string=dict(user="spongebob"))

        response_json = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

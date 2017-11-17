import json
import pdb
from flask import Flask, request, jsonify, make_response
from pymongo import MongoClient, ReturnDocument
from bson import Binary, Code
from bson.json_util import dumps
from flask_restful import Resource, Api

app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.trip_planer
api = Api(app)


class Users(Resource):

    def post(self):
        new_user = request.json
        users_collection = app.db.users
        result = users_collection.insert_one(new_user)
        user = users_collection.find_one({"_id": result.inserted_id})
        return user

    def get(self):
        user = request.args.get('user', type=str)
        users_collection = app.db.users
        user = users_collection.find_one({"user": user})
        # pdb.set_trace()
        if user is None:
            response = jsonify(data=[])
            response.status_code = 404
            return response
        else:
            return user

    def patch(self):
        user_name = request.args.get('user', type=str)
        new_user = request.args.get('new_user', type=str)
        users_collection = app.db.users
        user = users_collection.find_one_and_update(
            {"user": user_name},
            {"$set": {"user": new_user}},
            return_document=ReturnDocument.AFTER
        )
        if user is None:
            response = jsonify(data=[])
            response.status_code = 404
            return response
        else:
            return user

    def delete(self):
        user_name = request.args.get('name')
        users_collection = app.db.users
        users_collection.remove({'name': user_name})


class Trip(Resource):

    def __init__(self):
        self.trip_collection = app.db.trip

    def post(self):
        new_trip = request.json
        # trip_collection = app.db.trip
        result = self.trip_collection.insert_one(new_trip)
        trip = self.trip_collection.find_one({"_id": result.inserted_id})
        return trip

    def get(self):
        trip_name = request.args.get('trip_name')
        # trip_collection = app.db.trip
        trip = self.trip_collection.find_one({'trip_name': trip_name})
        return trip

    def patch(self):
        old_trip = request.args.get('old_trip')
        # trip_collection = app.db.trip
        new_trip = request.args.get('new_trip')
        trip = self.trip_collection.find_one_and_update(
            {'trip_name': old_trip},
            {"$set": {'trip_name': new_trip}},
            return_document=ReturnDocument.AFTER
        )
        return trip

    def delete(self):
        trip_name = request.args.get('trip_name')
        # trip_collection = app.db.trip
        self.trip_collection.remove({'trip_name': trip_name})



@api.representation('application/json')
def output_json(data, code, headers=None):
    resp = make_response(dumps(data), code)
    resp.headers.extend(headers or {})
    return resp


api.add_resource(Users, '/users/')
api.add_resource(Trip, '/trip')


if __name__ == '__main__':
    # Turn this on in debug mode to get detailled information about request related exceptions: http://flask.pocoo.org/docs/0.10/config/
    app.config['TRAP_BAD_REQUEST_ERRORS'] = True
    app.run(debug=True)

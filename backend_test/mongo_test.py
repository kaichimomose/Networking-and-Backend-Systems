import pdb
import json
from flask import Flask, request
from pymongo import MongoClient
from bson import Binary, Code
from bson.json_util import dumps
app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.local_test

# # Users from POST request
# users_dict = request.json
#
# # Our users collection
# users_collection = app.db.users
#
# # Inserting one user into our users collection
# result = users_collection.insert_one(
#     users_dict
# )


@app.route('/users', methods=['GET'])
def get_user_by_age():

    user_age_dict = request.args

    user_age = int(user_age_dict['age'])

    users_collection = app.db.users

    result = users_collection.find_one({'age': user_age})

    response_json = dumps(result)

    return (response_json, 200, None)


if __name__ == '__main__':
    app.run()
    app.config["Debug"] = True

import pdb
import json
from flask import Flask, request
from pymongo import MongoClient, ReturnDocument
# from bson import Binary, Code
from bson.json_util import dumps
from util import JSONEncoder
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


@app.route('/users', methods=['POST', 'GET'])
def get_or_post_users():
    # Our users collection
    users_collection = app.db.users
    if request.method == 'POST':
        # Users from POST request
        users_dict = request.json

        # Inserting one user into our users collection
        users_collection.insert_one(
            users_dict
        )
        json_result = JSONEncoder().encode(users_dict)
        return (json_result, 201, None)
    elif request.method == 'GET':
        name = request.args.get('name', type=str)
        result = users_collection.find_one(
            {'name': name}
        )
        response_json = JSONEncoder().encode(result)
        pdb.set_trace()
        return(response_json, 200, None)


@app.route('/courses', methods=['POST', 'GET'])
def get_or_post_courses():
    # Our users collection
    courses_collection = app.db.courses
    if request.method == 'POST':
        # Users from POST request
        courses_dict = request.json

        # Inserting one user into our users collection
        courses_collection.insert_one(
            courses_dict
        )
        json_result = JSONEncoder().encode(courses_dict)
        return (json_result, 201, None)
    elif request.method == 'GET':
        prams = request.args
        number = prams.get('number', type=int)
        if number is None:
            result = courses_collection.find()
        else:
            result = courses_collection.find_one(
                {'number': number}
            )
        response_json = dumps(result)
        if response_json == 'null':
            return("Error: There is no class assgined number:{}".format(number), 400, None)
        else:
            return(response_json, 200, None)


@app.route('/count_courses', methods=['GET'])
def count_courses():
    courses_collection = app.db.courses
    result = courses_collection.count()
    # pdb.set_trace()
    return("Number of courses: {}".format(result), 200, None)


@app.route('/carts', methods=['POST', 'PATCH', 'GET'])
def get_post_or_patch_carts():
    carts_collection = app.db.carts
    prams = request.args
    user = prams.get('user', type=str)
    brand = prams.get('brand', type=str)
    quantity = prams.get('quantity', type=int)
    if request.method == 'GET':
        if user is None:
            result = carts_collection.find()
        else:
            result = carts_collection.find_one(
                {'user': user}
            )
        response_json = dumps(result)
        if response_json == 'null':
            return('Error: There is no user named {}'.format(user), 400, None)
        else:
            return(response_json, 200, None)
    elif request.method == 'POST':
        carts_dict = request.json
        carts_collection.insert_one(
            carts_dict
        )
        json_result = JSONEncoder().encode(carts_dict)
        return (json_result, 201, None)
    elif request.method == 'PATCH':
        if user is not None and brand is not None and quantity is not None:
            result = carts_collection.find_one_and_update(
                {'user': user, 'items.brand': brand},
                {'$inc': {'items.$.quantity': quantity}},
                return_document=ReturnDocument.AFTER
            )
            response_json = JSONEncoder().encode(result)
            if response_json == 'null':
                result = carts_collection.find_one_and_update(
                    {'user': user},
                    {'$addToSet': {"items": {'brand': brand, 'quantity': quantity}}},
                    return_document=ReturnDocument.AFTER
                )
        response_json = JSONEncoder().encode(result)
        if response_json == 'null':
            return('Update failed', 400, None)
        else:
            return(response_json, 200, None)


if __name__ == '__main__':
    app.run()
    app.config["Debug"] = True

import pdb
import json
from flask import Flask, request
from pymongo import MongoClient
# from bson import Binary, Code
from bson.json_util import dumps
from util import JSONEncoder
app = Flask(__name__)
mongo = MongoClient('localhost', 27017)
app.db = mongo.test
pets_list = []

pet_1 = {"kind": "Ferret", "color": "glay"}
pet_2 = {"kind": "Rabbit", "color": "white"}
pets_list.append(pet_1)
pets_list.append(pet_2)


@app.route('/comments')
def hello_world():
    return 'Hello World!'


@app.route('/user')
def person_route():
    person = {"name": "Kaichi", 'age': 24}
    json_person = json.dumps(person)

    return (json_person, 200, None)


@app.route('/my_page')
def my_page_route():
    return "Hi, My name is Kaichi. I am a student at Make School"


@app.route('/pets')
def my_favorite_pets():
    # pet_1 = {"kind": "Ferret", "color": "glay"}
    # pet_2 = {"kind": "Rabbit", "color": "white"}
    # pets_list.append(pet_1)
    # pets_list.append(pet_2)
    json_pets = json.dumps(pets_list)
    # pdb.set_trace()

    return (json_pets, 200, None)


@app.route('/newpets', methods=['GET', 'POST'])
def add_pets():
    if request.method == 'POST':
        json_pets = json.dumps(request.json)
        return (json_pets, 201, None)


@app.route('/post_users', methods=['POST'])
def post_users():
    # Users from POST request
    users_dict = request.json
    # Our users collection
    users_collection = app.db.users

    # Inserting one user into our users collection
    result = users_collection.insert_one(
        users_dict
    )

    json_result = dumps(users_dict)
    # response_json = json.dumps(result)

    return (json_result, 201, None)


@app.route('/users', methods=['GET'])
def get_user():
    name = request.args.get('name', type=str)
    users_collection = app.db.users
    result = users_collection.find_one(
        {'name': name}
    )

    response_json = JSONEncoder().encode(result)

    # response_json = dumps(result)
    return (response_json, 200, None)

if __name__ == '__main__':
    app.run(debug=True)

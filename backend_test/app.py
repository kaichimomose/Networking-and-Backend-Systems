import pdb
import json
from flask import Flask, request
app = Flask(__name__)
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
    person = {"name": "Eliel", 'age': 23}
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


@app.route('/newpets', methods=['POST'])
def add_pets():
    # pdb.set_trace()
    body = json.loads(request.data)
    return pets_list


if __name__ == '__main__':
    app.run()
    app.config["Debug"] = True

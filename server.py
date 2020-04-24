from flask import Flask, render_template
from flask_cors import CORS
import connexion
from flask import jsonify, request
import os
import pymongo
from pymongo import MongoClient
import json


# Create the application instance
connx_app = connexion.App(__name__, specification_dir='./')

#url atlas
#mongodb+srv://people_user:xSyYV9Dbv269RYg@people-xq6tp.gcp.mongodb.net/people?retryWrites=true&w=majority

#url_local
mongo_uri = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']
# client = pymongo.MongoClient(os.environ['MONGODB_URI'])
client = pymongo.MongoClient(mongo_uri)
db = client.people


people_col = db.people
people_seq_col = db.people_sequence

# Read the swagger.yml file to configure the endpoints
# connx_app.add_api('swagger.yaml')

app = connx_app.app
cors = CORS(app, resources={r"*": {"origins": "*"}})

# Create a URL route in our application for "/"
@app.route('/')
def home():
    """
    This function just responds to the browser ULR
    localhost:5000/
    :return:        the rendered template 'home.html'
    """
    return render_template('home.html')

#method for search all people
@app.route('/people', methods=['GET'])
def list_people():
    print("[list_people]")
    people_list = list(people_col.find({}, {"_id": 0}))

    if len(people_list) > 0:
        return jsonify(people_list)
    else:
        return jsonify({'code':400,'message':'amount of people '+ str(len(people_list))})

#method for geting a person information
@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    people = people_col.find_one({"people_id": people_id},{"_id": 0})

    if people is None:
        return json.dumps({"code": 400, "message": "cant find person"})
    
    return json.dumps(people)

#method for creating a person
@app.route('/people', methods=['POST'])
def create_people():
    people_json = request.json
    print("[POST] JSON ", json.dumps(people_json))

    people_id = people_col.insert_one(people_json).inserted_id
    sequence = getValueForNextSequence("people_id")

    #sets and auto increment id to people
    people_col.find_one_and_update({"_id": people_id},{"$set": {"people_id": sequence}})

    return json.dumps({'code': 201, "message": "Created", "id": sequence})

#method for updating a person information
@app.route('/people/<int:people_id>', methods=['PUT'])
def update_people(people_id):
    people_json = request.json

    search_people = people_col.find_one({"people_id": people_id}, {"people_id": 1})

    if search_people is None:
        return json.dumps({"code": 400, "message": "Cant find person"})

    people_json["people_id"] = people_id
    people = people_col.replace_one({"people_id": int(people_id)}, people_json)


    return jsonify({'code':200,'message':'update ok'})

#method for delete a person
@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    
    people = people_col.find_one({"people_id": people_id})

    if people is None:
        return json.dumps({"code": 400, "message": "cant find person"})
    else:
        people_col.delete_one({"people_id": people_id})
    
    return json.dumps({"code": 200, "message": "people id "+str(people_id)+" deleted"})

#methos for using a sequence as and incfemental numeric id for each person
def getValueForNextSequence(people_id):
    seq = people_seq_col.find_one_and_update({'_id': people_id },
    {'$inc':{'sequence_value':1}},new = True)
    
    return seq["sequence_value"]
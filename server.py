from flask import Flask
from flask_cors import CORS
import connexion
from flask import jsonify, request, PyMongo
import os


# Create the application instance
connx_app = connexion.App(__name__, specification_dir='./')

# app.config["MONGO_URI"] = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + os.environ['MONGODB_PASSWORD'] + '@' + os.environ['MONGODB_HOSTNAME'] + ':27017/' + os.environ['MONGODB_DATABASE']

mongo = PyMongo(connx_app)
db = mongo.db

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

@app.route('/people', methods=['GET'])
def list_people():
    print("[list_people]")
    people_list = list(db.people.find({}))

    if len(people_list) > 0:
        return jsonify(people_list)
    else:
        return jsonify({'code':400,'message':'amount of people '+ str(len(people_list))})

@app.route('/people/<int:people_id>', methods=['GET'])
def get_people(people_id):
    return jsonify({'code':400,'message':'get_people not implemented yet'})

@app.route('/people', methods=['POST'])
def create_people():
    people_json = request.json
    print("[POST] json", people_json)
    return jsonify({'code':500,'message':'create_people not implemented yet'})

@app.route('/people/<int:people_id>', methods=['PUT'])
def update_people(people_id):
    people_json = request.json
    return jsonify({'code':500,'message':'update_people not implemented yet'})

@app.route('/people/<int:people_id>', methods=['DELETE'])
def delete_people(people_id):
    return jsonify({'code':500,'message':'delete_people not implemented yet'})
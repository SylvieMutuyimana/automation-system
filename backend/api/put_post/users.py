import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
from .. import dataset

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Fetch all userTypes from the JSON file
def return_dataset():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "../../dataset/users.json")
    with open(file_path) as file:
        data = json.load(file)    
    return data

CORS(app, resources={r"/users/*": {"origins": "http://localhost:3000"}})
@app.route('/addUser/<userType>', methods=['POST'])
def add_user(new_user, userType):
    new_user = request.json
    new_user['_id'] = str(uuid.uuid4())
    all_userTypeData = return_dataset()
    all_userTypeData[userType].append(new_user)
    try:
        with open(users_path, 'w') as json_file:
            try:
                json.dump(all_userTypeData, json_file)
                print('Session:\n', new_user, '\nadded successfully to:\n', users_path)
            except Exception as e:
                print("not added")
    except Exception as e:
        print('Error adding session:', str(e))
        print('Session data:', new_user)
    return jsonify(new_user), 200

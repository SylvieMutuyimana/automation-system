import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

current_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_dir, "../../dataset/users.json")

# Fetch all userTypes from the JSON file
def return_dataset():
    with open(file_path) as file:
        data = json.load(file)
    return data

@app.route('post/users/<userType>', methods=['POST'])
def add_user(userType):
    submittedData = request.json
    new_user = submittedData.get('new_user')
    
    if new_user is None:
        return jsonify({'error': 'Invalid JSON data'}), 400

    new_user['_id'] = str(uuid.uuid4())
    all_userTypeData = return_dataset()
    
    if userType in all_userTypeData:
        all_userTypeData[userType].append(new_user)
        try:
            with open(file_path, 'w') as json_file:
                json.dump(all_userTypeData, json_file, indent=4)
                print('User added successfully to:', userType)
        except Exception as e:
            print('Error adding user:', str(e))
            return jsonify({'error': 'Could not add user'}), 500
    else:
        return jsonify({'error': 'userType not found'}), 404
    
    return jsonify(new_user), 200

if __name__ == '__main__':
    app.run()

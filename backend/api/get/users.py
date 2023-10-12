import json
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})

# Fetch all userTypes from the JSON file
def return_dataset():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "../../dataset/users.json")
    with open(file_path) as file:
        data = json.load(file)    
    return data

# Fetch a specific userType from the JSON file based on userType
def get_allUsersTypeData(userType):
    all_users = return_dataset()
    userTypeData = all_users.get(userType, None)
    return userTypeData

# Fetch a specific user from the JSON file based on userEmail and userType
def getUserData(userType, userEmail):
    userTypeData = get_allUsersTypeData(userType)
    userData = next((user for user in userTypeData if user['email'] == userEmail), None)
    return userData

# Define route to get all userTypes
@app.route('/users', methods=['GET'])
def all_users():
    the_addresses = return_dataset()
    return jsonify(the_addresses)

# Define route to get a specific userType
@app.route('/users/<userType>', methods=['GET'])
def userTypeDataRoute(userType):
    userTypeData = get_allUsersTypeData(userType)
    if userTypeData:
        return jsonify(userTypeData)
    return jsonify({'error': 'userType not found'}), 404

# Define route to get a specific user of a specific userType
@app.route('/users/<userType>/<userEmail>', methods=['GET'])
def userDataRoute(userType, userEmail):
    userData = getUserData(userType, userEmail)
    if userData:
        return jsonify(userData)
    return jsonify({'error': 'user not found'}), 404

if __name__ == '__main__':
    app.run()
import json
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})

def return_dataset():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "../../dataset/requests.json")
    with open(file_path) as file:
        data = json.load(file)    
    return data

def getRequestData(requestID):
    all_requests = return_dataset()
    request_data = next((request for request in all_requests if request['_id'] == requestID), None)
    return request_data

def getFacilitatorRequests(facilitator):
    all_requests = return_dataset()
    facilitatorRequests = next((request for request in all_requests if request['facilitator'] == facilitator), None)
    return facilitatorRequests

def getStudentRequests(student):
    all_requests = return_dataset()
    studentRequests = next((request for request in all_requests if request['student'] == student), None)
    return studentRequests

@app.route('/requests', methods=['GET'])
def all_requests():
    the_requests = return_dataset()
    return jsonify(the_requests)

@app.route('/requests/<requestID>', methods=['GET'])
def requestDataRoute(requestID):
    request_data = getRequestData(requestID)
    if request_data:
        return jsonify(request_data)
    return jsonify({'error': 'request not found'}), 404

@app.route('/requests/facilitator/<facilitator>', methods=['GET'])
def FacilitatorrequestData(facilitator):
    facilitatorRequests = getFacilitatorRequests(facilitator)
    if facilitatorRequests:
        return jsonify(facilitatorRequests)
    return jsonify({'error': 'facilitator requests not found'}), 404

@app.route('/requests/student/<student>', methods=['GET'])
def StudentrequestData(student):
    studentRequests = getStudentRequests(student)
    if studentRequests:
        return jsonify(studentRequests)
    return jsonify({'error': 'student requests not found'}), 404

if __name__ == '__main__':
    app.run()
import json
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})

def return_dataset(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir,filename)
    with open(file_path) as file:
        data = json.load(file)    
    return data

def return_request_dataset():
    filename =  "../../dataset/requests.json"
    return return_dataset(filename)

def return_response_dataset():
    filename =  "../../dataset/responses.json"
    return return_dataset(filename)

def getResponseRequestData(requestID):
    all_responses = return_response_dataset()
    request_responses = all_responses.get(requestID)
    if request_responses:
        return request_responses
    else: return None

def getRequestData(requestID):
    all_requests = return_request_dataset()
    request_data = next((request for request in all_requests if request['_id'] == requestID), None)
    if request_data:
        return request_data
    else: return None
    
def getFacilitatorRequests(facilitator):
    all_requests = return_request_dataset()
    facilitatorRequests = [request for request in all_requests if request['facilitator'] == facilitator]
    if facilitatorRequests:
        return facilitatorRequests
    else: return None

def getStudentRequests(student):
    all_requests = return_request_dataset()
    studentRequests = [request for request in all_requests if request['student'] == student]
    if studentRequests:
        return studentRequests
    else: return None

@app.route('/requests', methods=['GET'])
def all_requests():
    the_requests = return_request_dataset()
    return jsonify(the_requests)

@app.route('/requests/<requestID>', methods=['GET'])
def requestDataRoute(requestID):
    request_data = getRequestData(requestID)
    if request_data:
        return jsonify(request_data)
    return jsonify({'error': 'request not found'}), 404

@app.route('/requests/<requestID>/responses', methods=['GET'])
def requestResponsesRoute(requestID):
    request_responses = getResponseRequestData(requestID)
    if request_responses:
        return jsonify(request_responses)
    return jsonify({'error': 'request responses not found'}), 404

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
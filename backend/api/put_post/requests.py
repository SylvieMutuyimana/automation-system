import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
import datetime

app = Flask(__name__)

def return_dataset(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, filename)
    return file_path

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

def return_data(file_path):
    with open(file_path) as file:
        data = json.load(file)
    return data

CORS(app, resources={r"/<student>/*": {"origins": "http://localhost:3000"}})
@app.route('/new_request/<student>', methods=['POST'])
def add_request(student):
    try:
        new_request = request.json
        new_request['student'] = student
        new_request['_id'] = str(uuid.uuid4())
        current_datetime = datetime.datetime.now()
        new_request['timestamp']  = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        file_path = return_dataset("../../dataset/requests.json")
        all_request_data = return_data(file_path)
        all_request_data.append(new_request)
        with open(return_dataset("../../dataset/requests.json"), 'w') as json_file:
            json.dump(all_request_data, json_file)
        return jsonify(new_request), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


CORS(app, resources={r"/<facilitator>/*": {"origins": "http://localhost:3000"}})
@app.route('/requests/<requestID>/responses', methods=['POST'])
def add_response(requestID):
    try:
        new_response = request.json
        new_response['_id'] = str(uuid.uuid4())
        current_datetime = datetime.datetime.now()
        new_response['timestamp']  = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        file_path = return_dataset("../../dataset/responses.json")
        all_request_data = return_data(file_path)
        print("all_request_data: ", all_request_data)
        if requestID in all_request_data:
            print('appending')
            all_request_data[requestID].append(new_response)
        else:
            print('the new one')
            all_request_data[requestID] = [new_response]
        print("\n\n\n\nnew: ", all_request_data)
        with open(return_dataset("../../dataset/responses.json"), 'w') as json_file:
            json.dump(all_request_data, json_file)
        return jsonify(new_response), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
from .. import dataset

app = Flask(__name__)

chargers_path = dataset.file_paths['chargers_path']
stations_data = dataset.read_dataset(dataset.file_paths["chargers_path"])
all_stations = stations_data['Stations']

CORS(app, resources={r"/Stations/*": {"origins": "http://localhost:3000"}})
@app.route('/Stations/<int:station_id>/chargers/<int:charger_id>', methods=['PUT'])
def change_charger_status():
    charger_info = request.json
    charger_id = charger_info.get('chargerid')
    user = charger_info.get('user')
    station_id = charger_info.get('stationid')
    if not charger_id:
        return jsonify({"message": "Charger ID not provided"}), 400
    for station in all_stations:
        if(station['id'] == station_id):
            print('they are equal')
            for charger in station['chargers']:
                if charger['id'] == charger_id:
                    charger['active'] = not charger['active']
                    charger['active_user'] = '' if charger['active'] else user
    try:
        with open(chargers_path, 'w') as json_file:
            json.dump(stations_data, json_file)
            print('Charger status updated successfully')
    except Exception as e:
        print('Error updating charger status:', str(e))

    return jsonify({"message": "Charger status updated"}), 200

if __name__ == '__main__':
    app.run()

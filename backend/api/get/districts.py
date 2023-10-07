import json
from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/*":{"origins":"*"}})

# Fetch all provinces from the JSON file
def return_dataset():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "../../dataset/districts.json")
    with open(file_path) as file:
        data = json.load(file)    
    return data

# Fetch a specific province from the JSON file based on provinceName
def get_provinceData(provinceName):
    provinces = return_dataset()
    province_data = provinces.get(provinceName, None)
    return province_data

# Fetch a specific district from the JSON file based on districtName and provinceName
def get_districtData(provinceName, districtName):
    province_data = get_provinceData(provinceName)
    district_data = province_data.get(districtName, None)
    return district_data

# Fetch a specific district from the JSON file based on districtName and provinceName
def get_sectorData(provinceName, districtName, sectorName):
    province_data = get_provinceData(provinceName)
    district_data = province_data.get(districtName, None)
    sector_data = district_data.get(sectorName, None)
    return sector_data

# Define route to get all provinces
@app.route('/location', methods=['GET'])
def all_addresses():
    the_addresses = return_dataset()
    return jsonify(the_addresses)

# Define route to get a specific province
@app.route('/location/<provinceName>', methods=['GET'])
def provinceDataRoute(provinceName):
    province_data = get_provinceData(provinceName)
    if province_data:
        return jsonify(province_data)
    return jsonify({'error': 'province not found'}), 404

# Define route to get a specific district of a specific province
@app.route('/location/<provinceName>/<districtName>', methods=['GET'])
def districtDataRoute(provinceName, districtName):
    district_data = get_districtData(provinceName, districtName)
    if district_data:
        return jsonify(district_data)
    return jsonify({'error': 'district not found'}), 404

# Define route to get a specific district of a specific province
@app.route('/location/<provinceName>/<districtName>/<sectorName>', methods=['GET'])
def sectorDataRoute(provinceName, districtName, sectorName):
    sector_data = get_sectorData(provinceName, districtName, sectorName)
    if sector_data:
        return jsonify(sector_data)
    return jsonify({'error': 'sector not found'}), 404

if __name__ == '__main__':
    app.run()
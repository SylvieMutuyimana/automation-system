import os
import json
from flask import Flask, jsonify, request
from flask_cors import CORS
import uuid
import bcrypt
import jwt  # Import the JWT library

app = Flask(__name__)
SECRET_KEY = 'your_secret_key_here'  # Replace with your actual secret key

def return_dataset():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, "../../dataset/users.json")
    return file_path

CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Fetch all userTypes from the JSON file
def return_data():
    file_path = return_dataset()
    with open(file_path) as file:
        data = json.load(file)
    return data

# Function to generate a JWT token
def generate_token(email, user_type):
    payload = {'email': email, 'user_type': user_type}
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

@app.route('/<userType>', methods=['POST'])
def add_user(userType):
    try:
        new_user = request.json
        all_user_data = return_data()
        for user_type in all_user_data:
            for user in all_user_data[user_type]:
                if user.get('email') == new_user['email']:
                    return jsonify({"message": f"{new_user['email']} already exists"}), 400
        
        new_user['_id'] = str(uuid.uuid4())
        # Hash the password before storing it
        password = new_user.get('password')
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        new_user['password'] = hashed_password.decode('utf-8')  # Store the hashed password
        
        all_user_data = return_data()
        all_user_data[userType].append(new_user)
        
        with open(return_dataset(), 'w') as json_file:
            json.dump(all_user_data, json_file)
        
        return jsonify(new_user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        login_data = request.json
        email = login_data.get('email')
        password = login_data.get('password')
        all_user_data = return_data()
        
        for user_type in all_user_data:
            for user in all_user_data[user_type]:
                if user.get('email') == email:
                    stored_password = user.get('password').encode('utf-8')
                    if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                        # Generate a token upon successful login
                        token = generate_token(email, user_type)
                        return jsonify({"email": email, "userType": user_type, "token": token}), 200
        
        raise Exception("Invalid email or password")
    except Exception as e:
        return jsonify({"error": str(e)}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

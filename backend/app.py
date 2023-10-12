from flask import Flask
from flask_cors import CORS
from api.get.districts import all_addresses, provinceDataRoute, districtDataRoute, sectorDataRoute
from api.get.users import all_users, userTypeDataRoute, userDataRoute 
from api.get.requests import all_requests, requestDataRoute, FacilitatorrequestData, StudentrequestData, requestResponsesRoute
from api.put_post.users import add_user, login
from api.put_post.requests import add_request, add_response

# Read the URL from the ip_address.txt file
ip_file = "localhost_ip.txt"
with open(ip_file, "r") as file:
    url = file.read().strip()

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})  # Allow CORS for all routes and origins


# Define route for root URL
@app.route("/", methods=["GET"])
def root():
    return (    
        "Welcome to the API! <br>"
        "Visit <a href='/location'>/location</a> to get all locations.<br>"
        "Visit <a href='/users'>/users</a> to get all users.<br>"
        "Visit <a href='/requests'>/requests</a> to get all requests.<br>"
        "<br>POSTING<br>"
        "Visit <a href='/addUser'>addUser</a> to addUser.<br>"
    )

# Location routes
app.add_url_rule("/location", "all_addresses", all_addresses, methods=["GET"])
app.add_url_rule("/location/<provinceName>", "provinceDataRoute", provinceDataRoute, methods=["GET"])
app.add_url_rule("/location/<provinceName>/<districtName>", "districtDataRoute", districtDataRoute, methods=["GET"])
app.add_url_rule("/location/<provinceName>/<districtName>/<sectorName>", "sectorDataRoute", sectorDataRoute, methods=["GET"])

# Users routes
app.add_url_rule("/users", "all_users", all_users, methods=["GET"])
app.add_url_rule("/users/<userType>", "userTypeDataRoute", userTypeDataRoute, methods=["GET"])
app.add_url_rule("/users/<userType>/<userEmail>", "userDataRoute", userDataRoute, methods=["GET"])

# requests routes
app.add_url_rule("/requests", "all_requests", all_requests, methods=["GET"])
app.add_url_rule("/requests/<requestID>", "requestDataRoute", requestDataRoute, methods=["GET"])
app.add_url_rule("/requests/<requestID>/responses", "requestResponsesRoute", requestResponsesRoute, methods=["GET"])
app.add_url_rule("/requests/<requestID>/responses", "add_response", add_response, methods=["POST"])
app.add_url_rule("/requests/student/<student>", "StudentrequestData", StudentrequestData, methods=["GET"])
app.add_url_rule("/requests/facilitator/<facilitator>", "FacilitatorrequestData", FacilitatorrequestData, methods=["GET"])

app.add_url_rule("/<userType>", "add_user", add_user, methods=["POST"])
app.add_url_rule("/login", "login", login, methods=["POST"])

app.add_url_rule("/new_request/<student>", "add_request", add_request, methods=["POST"])

if __name__ == "__main__":
    app.run(host=url, port=5001)

from flask import Flask
from flask_cors import CORS
from api.get.districts import all_addresses, provinceDataRoute, districtDataRoute, sectorDataRoute
from api.get.users import all_users, userTypeDataRoute, userDataRoute 

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
        "<br>POSTING<br>"
        "Visit <a href='/addSession'>addSession</a> to addSession.<br>"
        "Visit <a href='/updateSession'>addSession</a> to updateSession.<br>"
    )

# Location routes
app.add_url_rule("/location", "all_addresses", all_addresses, methods=["GET"])
app.add_url_rule("/location/<provinceName>", "provinceDataRoute", provinceDataRoute, methods=["GET"])
app.add_url_rule("/location/<provinceName>/<districtName>", "districtDataRoute", districtDataRoute, methods=["GET"])
app.add_url_rule("/location/<provinceName>/<districtName>/<sectorName>", "sectorDataRoute", sectorDataRoute, methods=["GET"])

# Users routes
app.add_url_rule("/users", "all_users", all_users, methods=["GET"])
app.add_url_rule("/users/<userType>", "userTypeDataRoute", userTypeDataRoute, methods=["GET"])
app.add_url_rule("/users/<userType>/<userId>", "userDataRoute", userDataRoute, methods=["GET"])

if __name__ == "__main__":
    app.run(host=url, port=5001)

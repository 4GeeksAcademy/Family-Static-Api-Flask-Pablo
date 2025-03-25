"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)


jackson_family = FamilyStructure("Jackson")

#Members

John = {
    "first_name": John,
    "last_name": Jackson,
    "age": 33,
    "lucky_numbers": [7, 13, 22]
}

Jane = {
    "first_name": Jane,
    "last_name": Jackson,
    "age": 35,
    "lucky_numbers": [10, 14, 3]
}

Jimmy = {
    "first_name": Jimmy,
    "last_name": Jackson,
    "age": 5,
    "lucky_numbers": [1]
}
jackson_family.add_member(John)
jackson_family.add_member(Jane)
jackson_family.add_member(Jimmy)

@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

#Method GET
@app.route('/members', methods=['GET'])
def handle_hello():

    members = jackson_family.get_all_members()
    response_body = {
        "hello": "world",
        "family": members
    }

    return jsonify(response_body), 200

#Method GET(id)
@app.route('/members/<int:id>', methods=['GET'])
def handle_hello(id):

    members = jackson_family.get_member(id)
    if not members:
        return jsonify({"Error": "Member not found"}), 404
    response_body = {
        "hello": "world",
        "family": members
    }

    return jsonify(response_body), 200

#Method DELETE
@app.route('/members/<int:id>', methods=['DELETE']) #Metodo Delete
def delete_member(id):
    members = jackson_family.delete_member(id)
    response_body = {
        "Messager": "Member Delete"
    }

    return jsonify(response_body), 200

#Method POST
@app.route('/members', methods=['POST'])
def add_new_member():
    request_body = request.json
    if not request_body:
       return jsonify({"error": "Invalid input"}), 400
    new_member = jackson_family.add_member(request_body)
    return jsonify(new_member), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
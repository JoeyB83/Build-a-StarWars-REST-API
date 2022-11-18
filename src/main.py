"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/user', methods=['GET'])
def handle_hello():

    users_query = User.query.all()

    all_user = list(map(lambda x: x.serialize(), users_query))

    return jsonify(all_user), 200

@app.route('/user', methods=['POST'])
def createUser():

    body = request.get_json()
    if body is None:
        return "The request body is null", 400
    if 'email' not in body:
        return "Add the user email", 400
    if 'password' not in body:
        return "Add user password", 400
    if 'Is_active' not in body:
        return "Add if the user is active", 400

    new_user = User(email=body["email"], password=body["password"], is_active=body["Is_active"])
    db.session.add(new_user)   
    db.session.commit()             
    
    return 'User was added', 200   

# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)

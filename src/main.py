"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from models import db,ToDo
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_CONNECTION_STRING')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)

@app.route('/todo', methods=['POST', 'GET'])
def handle_todo():

    if request.method == "POST":
        body = request.get_json()
        
        if body is None:
            raise APIException("You need to specify the request body as a json object",status_code = 400)
        if "label" not in body:
            raise APIException("You need to specify a todo", status_code = 400)
       
        
        todo1 = ToDo(label=body["label"],done=body["false"])
        db.session.add(todo1)
        db.session.commit()

        return "Ok", 200
    
    #Get Request
    if request.method == "GET":
        
        all_todo = ToDo.query.all()
        all_todo = list(map(lambda x : x.serialize(), all_todo))
        return jsonify(all_todo), 200

    return "Invalid Method", 404

 
@app.route('/todo/<int:todo_id>', methods=['PUT', 'GET','DELETE'])
def single_contact(todo_id):

    #PUT Request
    if request.method == "PUT":

        body = request.get_json()
        
        if body is None:
            raise APIException("You need to specify the request body as a json object",status_code = 400)
        todo1 = ToDo.query.get(todo_id)
        if todo1 is None:
            raise APIException("to do not found!",404)
        
        if "label" in body:
            todo1.name = body["label"]
        
        
        db.session.commit()

        return jsonify(todo1.serialize()),200 

    #GET method
    if request.method == "GET":
        contact1 = ToDo.query.get(todo_id)
        if todo1 is None:
            raise APIException("Label not found!", status_code = 404)

        return jsonify(todo1.serialize()),200
        
    #DELETE method
    if request.method == "DELETE":
        todo1 = ToDo.query.get(todo_id)
        if todo1 is None:
            raise APIException("To do  not found!", status_code = 404)

        db.session.delete(todo1)
        db.session.commit()

        return "Ok",200
        
    return "Invalid method", 404







# this only runs if `$ python src/main.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
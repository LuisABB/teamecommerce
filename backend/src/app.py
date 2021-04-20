from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo, ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from bson import json_util
from flask_cors import CORS


app = Flask(__name__)

app.config['MONGO_URI'] = 'mongodb://localhost/pythonmongodb'
mongo = PyMongo(app)
CORS(app)
db=mongo.db.users

@app.route('/users', methods=['POST'])
def createUser():
    id = db.insert({
        'name': request.json['name'],
        'email': request.json['email'], 
        'password': request.json['password']
    })
    return jsonify(str(ObjectId(id)))

@app.route('/users', methods=['GET'])
def getUsers():
    users = []
    for doc in db.find():
        users.append({
            '_id': str(ObjectId(doc['_id'])),
            'name': doc['name'],
            'email': doc['email'],
            'password': doc['password']
        })
    return jsonify(users)

@app.route('/users/<id>', methods=['GET'])
def getUser(id):
    user = db.find_one({'_id':ObjectId(id)})
    print(user)
    return jsonify({
        '_id': str(ObjectId(user['_id'])),
            'name': user['name'],
            'email': user['email'],
            'password': user['password']

    })

@app.route('/users/<id>', methods=['DELETE'])
def deleteUser(id):
    db.delete_one({'_id': ObjectId(id)})
    return jsonify({'msg':'User deleted'})

@app.route('/users/<id>', methods=['PUT'])
def updateUser(id):
    db.update_one({'_id':ObjectId(id)}, {'$set':{
        'name': request.json['name'],
        'email': request.json['email'], 
        'password': request.json['password']
    }})
    return jsonify({'msg':'User Updated'})
'''
@app.errorhandler(404)
def not_found(error=None):
    response = jsonify({
        'message': 'Resource Not Found' + request.url,
        'status':404
    })
    response.status_code = 404
    return response'''


if __name__ == "__main__":
    app.run(debug=True)
import os
from services.connect import *
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from dotenv import load_dotenv

load_dotenv()

user_blueprint = Blueprint('users', __name__)

MONGODB_CONNECTION_STRING = os.getenv("MONGO_URI")
MONGODB_DATABASE = 'ch'

# GET All users


@user_blueprint.route('/users', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
def show_all_users():
    client, collection = connect_mongo('users')
    # get all users from mongodb using
    result = []

    for user in collection.find():

        result.append({
            '_id': user['_id'],
            'name': user['name'],
            'email': user['email'],
            'photoURL': user['photoURL']
        })
    # close the connection to mongodb
    client.close()
    return result, 200

# GET single user


@user_blueprint.route('/user/<uid>', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
def show_single_users(uid):
    client, collection = connect_mongo('users')
    useriter = collection.find({'_id': uid})
    cur_user = {}
    for user in useriter:

        cur_user = {
            '_id': user['_id'],
            'name': user['name'],
            'email': user['email'],
            'photoURL': user['photoURL']
        }

    # close the connection to mongodb
    client.close()

    return jsonify(cur_user), 200

# POST create a user


@user_blueprint.route('/users', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
def create_user():

    data = request.get_json()
    client, collection = connect_mongo('users')

    newUser = {}
    newUser['_id'] = data['uid']
    newUser['name'] = data['name']
    newUser['email'] = data['email']
    newUser['photoURL'] = data['photoURL']

    collection.insert_one(newUser)
    client.close()

    return jsonify(newUser), 201

# POST Sign In


@user_blueprint.route('/login', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
def sign_in():
    return jsonify({
        'message': 'Sign In'
    }), 200

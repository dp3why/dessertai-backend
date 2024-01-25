import os
from services.connect import *
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from dotenv import load_dotenv
import uuid

load_dotenv()

review_blueprint = Blueprint('reviews', __name__)

MONGODB_CONNECTION_STRING = os.getenv("MONGO_URI")
MONGODB_DATABASE = 'ch'

# POST create a user


@review_blueprint.route('/reviews', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
def create_review():

    data = request.get_json()
    client, collection = connect_mongo('reviews')

    newReview = {}
    newReview['_id'] = uuid.uuid4()
    newReview['title'] = data['title']
    newReview['ratings'] = data['ratings']
    newReview['content'] = data['content']

    collection.insert_one(newReview)
    client.close()

    return jsonify(newReview), 201

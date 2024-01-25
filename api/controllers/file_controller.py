import os
from services.connect import *
from services.upload_service import *
from flask import Blueprint, jsonify, request
from flask_cors import cross_origin
from dotenv import load_dotenv
import uuid

load_dotenv()

file_blueprint = Blueprint('files', __name__)

MONGODB_CONNECTION_STRING = os.getenv("MONGO_URI")
MONGODB_DATABASE = 'ch'

# POST: upload a file to mongodb and to s3


@file_blueprint.route('/upload', methods=['POST'])
@cross_origin(headers=['Content-Type', 'Authorization'])
def upload_file():
    if 'file' not in request.files:
        return jsonify(error='No file part'), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify(error='No selected file'), 400

    # Upload file to AWS S3
    file_url = upload_file_to_s3(file)

    # Save file URL to MongoDB
    file_id = uuid.uuid4().hex
    uid = request.form.get('uid')
    username = request.form.get('username')
    save_file_url_to_mongodb(file_id, file.filename, file_url, username, uid)

    # Return the response as JSON
    return jsonify(
        message='File uploaded successfully',
        file_id=file_id,
        filename=file.filename,
        username=username,
        uid=uid,
        url=file_url
    ), 200

# GET find all files


@file_blueprint.route('/files', methods=['GET'])
@cross_origin(headers=['Content-Type', 'Authorization'])
def get_files():

    files = get_all_files_from_mongodb()
    if files:
        return jsonify(files)
    return []


# DELETE file

@file_blueprint.route('/files', methods=['DELETE'])
@cross_origin(headers=['Content-Type', 'Authorization'])
def delete_file():
    data = request.get_json()
    if 'url' not in data:
        return jsonify(error='No file url'), 400
    uid = data.get('uid')
    file_url = data.get('url')
    file_name = file_url.split('/')[-1]

    # Delete file from MongoDB
    mongo_res = delete_file_from_mongodb(file_url, uid)

    # Delete file from AWS S3
    if mongo_res:
        s3_res = delete_file_from_s3(file_name)
    else:
        s3_res = False

    if mongo_res and s3_res:
        # Return the response as JSON
        return jsonify(
            message='File deleted successfully',
            filename=file_name
        ), 200
    if mongo_res:
        return jsonify(error='mongo deleted, s3 failed, Failed to deleted'), 400
    else:
        return jsonify(error='Both Failed to deleted'), 400

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
import os

load_dotenv()

MONGODB_CONNECTION_STRING = os.getenv("MONGO_URI")
MONGODB_DATABASE = 'ch'

# connect to mongodb


def connect_mongo(collection_name):
    client = MongoClient(MONGODB_CONNECTION_STRING,  tls=True,
                         tlsAllowInvalidCertificates=True)
    db = client[MONGODB_DATABASE]
    collection = db[collection_name]

    return client, collection


def save_file_url_to_mongodb(file_id, filename, url, username, uid):
    client, collection = connect_mongo('upload')
    document = {
        '_id': file_id,
        'filename': filename,
        'url': url,
        'username': username,
        'uid': uid,
    }
    collection.insert_one(document)
    client.close()


def get_all_files_from_mongodb():
    client, collection = connect_mongo('upload')

    files = collection.find()

    file_list = []
    for file in files:
        file_info = {
            '_id': file['_id'],
            'filename': file['filename'],
            'url': file['url'],
            'username': file['username'],
            'uid': file['uid'],
        }
        file_list.append(file_info)

    client.close()
    return file_list


def delete_file_from_mongodb(file_url, uid):
    client, collection = connect_mongo('upload')
    # locate the file first, if not, return false
    if collection.find_one({'url': file_url, 'uid': uid }) is None:
        return False
    # delete the file
    result = collection.delete_one({'url': file_url, 'uid': uid})

    client.close()
    if result.deleted_count == 1:
        return True
    else:
        return False

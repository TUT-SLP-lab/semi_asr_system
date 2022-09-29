import pymongo
from bson.objectid import ObjectId
import requests
import datetime
import os
from dotenv import load_dotenv


def create_dummy_data():
    load_dotenv()

    DB_PLACE = "localhost"  # os.getenv("MONGO_DB_SERVER")
    DB_PORT = os.getenv("MONGO_DB_PORT")
    DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
    DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")

    client = pymongo.MongoClient(DB_PLACE, int(DB_PORT), username=DB_USERNAME, password=DB_PASSWORD)

    db = client[os.getenv("MONGO_DB_NAME")]
    collection = db[os.getenv("MONGO_COLLECTION_NAME")]
    post = {
        "attribute": "2022-08-19_test_record_004",
        "audio_path": f"{os.getenv('WAV_DIR')}/2022-08-19_test_record_004_44100.wav",
        "text_path": "",
        "status": "unprocessed",
        "add_date": "",
    }
    post_id = collection.insert_one(post).inserted_id

    return str(post_id)

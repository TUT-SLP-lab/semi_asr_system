import pymongo
from bson.objectid import ObjectId
import requests
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

DB_PLACE = "localhost"  # os.getenv("MONGO_DB_SERVER")
DB_PORT = os.getenv("MONGO_DB_PORT")
DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")

client = pymongo.MongoClient(DB_PLACE, int(DB_PORT), username=DB_USERNAME, password=DB_PASSWORD)


db = client[os.getenv("MONGO_DB_NAME")]
collection = db[os.getenv("MONGO_COLLECTION_NAME")]
post = {
    "attribute": "test",
    "audio_path": "test/test.wav",
    "text_path": "unprocessed",
    "status": "unprocessed",
    "add_date": "unprocessed",
}
post_id = collection.insert_one(post).inserted_id

print(post_id)

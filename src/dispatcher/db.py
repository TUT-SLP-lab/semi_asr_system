import pymongo
from bson.objectid import ObjectId

mongoURL = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongoURL)

db = client["asr_queue"]
collection = db["queue"]


def updateTextFilePath(_id, path):
    id = ObjectId(_id)
    response = collection.update_one({"_id": id}, {"$set": {"text_path": path, "status": "completed"}})
    return response.modified_count


def getAudioData(_id):
    id = ObjectId(_id)
    response = collection.find_one({"_id": id})
    collection.update_one({"_id": id}, {"$set": {"status": "processing"}})
    pooling_data = {"attribute": response["attribute"], "audio_path": response["audio_path"]}
    return pooling_data

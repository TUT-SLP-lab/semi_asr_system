import pymongo
from bson.objectid import ObjectId

mongoURL = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongoURL)

db = client["asr_queue"]
collection = db["queue"]


def updateTextFilePath(path):
    check_process_queue = collection.find_one({"status": "processing"})

    if check_process_queue:
        id = ObjectId(check_process_queue["_id"])
        response = collection.update_one({"_id": id}, {"$set": {"text_path": path, "status": "completed"}})
        return response.modified_count
    else:
        return "not processing queue"


def postAudioData(_id):
    id = ObjectId(_id)
    response = collection.find_one({"_id": id})
    collection.update_one({"_id": id}, {"$set": {"status": "processing"}})
    pooling_data = {"attribute": response["attribute"], "audio_path": response["audio_path"]}
    return pooling_data


def postRecordData(_id):
    # id = ObjectId(_id)
    check_process_status = collection.find_one({"status": "processing"})
    if check_process_status:
        return "processing now"
    else:
        data = postAudioData(_id)
        return data

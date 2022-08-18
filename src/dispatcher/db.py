import pymongo

mongoURL = "mongodb://localhost:27017"
client = pymongo.MongoClient(mongoURL)

db = client["asr_queue"]
collection = db["queue"]


# def createAudioData(data):
#     data = dict(data)
#     response = collection.insert_one(data)
#     return str(response.inserted_id)


# def getAudioData(data):
#     response = collection.find_one({"attribute": data})
#     response["_id"] = str(response["_id"])
#     return response


# mock_data = {"attribute": "test3", "audio_path": "/test/hoge4.wave"}

# collection.insert_one(mock_data)

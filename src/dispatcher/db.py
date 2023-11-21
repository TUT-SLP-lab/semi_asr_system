import pymongo
from bson.objectid import ObjectId
import requests
import datetime
import os
import json
from dotenv import load_dotenv

load_dotenv()

DB_PLACE = os.getenv("MONGO_DB_SERVER")
DB_PORT = os.getenv("MONGO_DB_PORT")
DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")

client = pymongo.MongoClient(DB_PLACE, int(DB_PORT), username=DB_USERNAME, password=DB_PASSWORD)

db = client[os.getenv("MONGO_DB_NAME")]
collection = db[os.getenv("MONGO_COLLECTION_NAME")]
baseurl = f"http://{os.getenv('ASR_SYSTEM_IP')}:{os.getenv('ASR_SYSTEM_PORT')}/api"  # ASRシステムへの送り先（未定）


# text_pathとstatusを更新する
def updateTextFilePath(path):
    check_process_queue = collection.find_one({"status": "processing"})
    # processingのqueueがあった時
    if check_process_queue:
        id = ObjectId(check_process_queue["_id"])
        response = collection.update_one({"_id": id}, {"$set": {"text_path": path.text_path, "status": "completed"}})
        return response.modified_count
    # processingのqueueがなかった時
    else:
        return "not processing queue"


def getNextProcessId():
    check_unprocessed_queue = collection.find_one({"status": "unprocessed"})
    if not check_unprocessed_queue:
        return None
    return check_unprocessed_queue["_id"]


# _idからデータを取得してASRシステムに送る
def postAudioData(id):
    id = ObjectId(id)
    response = collection.find_one({"_id": id})
    if not response:
        return "This id is None"
    if response["status"] == "completed":
        return "This id is completed"

    print("send data to asr system")
    pooling_data = {"attribute": response["attribute"], "audio_path": response["audio_path"]}
    result = requests.post(f"{baseurl}/inference", json=pooling_data)
    print(f"asr system response: {result.json()}")
    collection.update_one({"_id": id}, {"$set": {"status": "processing", "add_time": datetime.datetime.now()}})
    return "pooling"


# 録音しているところから_idを受け取る
def postRecordData(id):
    check_process_status = collection.find_one({"status": "processing"})
    if check_process_status:
        return "processing now"
    else:
        data = postAudioData(id)
        return data


def reRun():
    processing_data = collection.find_one({"status": "processing"})
    if processing_data:
        return postAudioData(processing_data["_id"])
    check_unprocessed_queue = collection.find_one({"status": "unprocessed"})
    if check_unprocessed_queue:
        return postAudioData(check_unprocessed_queue["_id"])


# 定期実行されるべきもの
def DeleteAndSurveillance():
    processing_data = collection.find_one({"status": "processing"})
    if processing_data:
        if abs(processing_data["add_time"] - datetime.datetime.now()).days >= 1:
            # 1日以上processingがあったら送り直し
            pooling_data = {"attribute": processing_data["attribute"], "audio_path": processing_data["audio_path"]}
            result = requests.post(f"{baseurl}/inference", json=pooling_data)
            print(result.json())
            collection.update_one({"_id": processing_data["_id"]}, {"$set": {"add_time": datetime.datetime.now()}})
            print("processing ok")

    if not processing_data:
        # processingがなかったらタスクを投げる
        unprocessed_data = collection.find_one({"status": "unprocessed"})
        if unprocessed_data:
            id = unprocessed_data["_id"]
            postAudioData(id)
            print("process start")

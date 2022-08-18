from fastapi import FastAPI
import db
import requests

app = FastAPI()


@app.put("/api/update")
def updateTextFilePath(path):
    data = db.updateTextFilePath(path)
    return {"updated": True, "updated_count": data}


# @app.post("/api/audio")
# def postAudioData(_id):
#     data = db.getAudioData(_id)
#     return data


@app.post("/api/id")
def postRecordData(_id):
    data = db.postRecordData(_id)
    return data

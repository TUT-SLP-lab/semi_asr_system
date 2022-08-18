from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import db
import models

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/create")
def createAudioData(data: models.Audio):
    id = db.createAudioData(data)
    return {"id": id}


@app.put("/update")
def updateTextFilePath(_id, path):
    data = db.updateTextFilePath(_id, path)
    return {"updated": True, "updated_count": data}


@app.get("/audio")
def getAudioASRData(_id):
    data = db.getAudioData(_id)
    return data

from fastapi import FastAPI
import db
import uvicorn
from pydantic import BaseModel
import os
from dotenv import load_dotenv

app = FastAPI()
load_dotenv()
DISPATCHER_PORT = os.getenv("DISPATCHER_PORT")



class Item(BaseModel):
    id: str


class Path(BaseModel):
    text_path: str


@app.put("/api/update")
def updateTextFilePath(path: Path):
    print("update text file path is called")
    data = db.updateTextFilePath(path)
    return {"updated": True, "updated_count": data}


# @app.post("/api/audio")
# def postAudioData(_id):
#     data = db.getAudioData(_id)
#     return data


@app.post("/api/id")
def postRecordData(item: Item):
    print("postRecordData is called")
    data = db.postRecordData(item.id)
    return data


@app.delete("/api/delete")
def ScheduledExecution():
    print("Scheduled Execution is called")
    db.DeleteAndSurveillance()


uvicorn.run(app, host="0.0.0.0", port=DISPATCHER_PORT)
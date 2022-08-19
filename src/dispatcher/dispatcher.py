from fastapi import FastAPI
import db
import uvicorn
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    id: str

class Path(BaseModel):
    text_path: str

@app.put("/api/update")
def updateTextFilePath(path: Path):
    data = db.updateTextFilePath(path)
    return {"updated": True, "updated_count": data}

# @app.post("/api/audio")
# def postAudioData(_id):
#     data = db.getAudioData(_id)
#     return data

@app.post("/api/id")
def postRecordData(item: Item):
    data = db.postRecordData(item)
    return data

@app.delete("/api/delete")
def ScheduledExecution():
    db.DeleteAndSurveillance()


uvicorn.run(app, host="0.0.0.0", port=5001)


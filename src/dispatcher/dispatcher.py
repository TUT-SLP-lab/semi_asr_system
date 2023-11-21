from fastapi import FastAPI
import db
import uvicorn
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from time import sleep

app = FastAPI()
load_dotenv()
DISPATCHER_PORT = int(os.getenv("DISPATCHER_PORT"))


class Item(BaseModel):
    id: str


class Path(BaseModel):
    text_path: str


@app.put("/api/update")
def updateTextFilePath(path: Path):
    print("update text file path is called")
    try:
        data = db.updateTextFilePath(path)
        yield {"updated": True, "updated_count": data}
    finally:
        # 追加で新しい音声を処理する
        next_id = db.getNextProcessId()
        if next_id:
            sleep(60)  # ASRサーバーの処理が完了するまで待つ
            print("Do next audio")
            db.postRecordData(next_id)


# @app.post("/api/audio")
# def postAudioData(_id):
#     data = db.getAudioData(_id)
#     return data


@app.post("/api/id")
def postRecordData(item: Item):
    print("postRecordData is called")
    data = db.postRecordData(item.id)
    return data


@app.post("/api/rerun")
def reRun():
    print("reRun is called")
    return db.reRun()


# 使用しないので、コメントアウト
# @app.delete("/api/delete")
# def ScheduledExecution():
#     print("Scheduled Execution is called")
#     db.DeleteAndSurveillance()


uvicorn.run(app, host="0.0.0.0", port=DISPATCHER_PORT)

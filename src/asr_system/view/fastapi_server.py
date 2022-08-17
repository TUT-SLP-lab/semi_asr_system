from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel

from asr_system.controller import Controller

app = FastAPI()


class Audio(BaseModel):
    attribute: str
    audio_path: str


job = Controller()


@app.get("/api/inference")
async def asr_inference(audio: Audio, background_task: BackgroundTasks):

    if job.is_running is False:
        background_task.add_task(job.speech2text)

        return {
            "attribute": audio.attribute,
            "audio_path": audio.audio_path,
            "text_path": audio.text_path,
        }
    return {"message": "job is running"}

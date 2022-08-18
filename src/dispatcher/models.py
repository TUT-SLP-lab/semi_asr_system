from pydantic import BaseModel


class Audio(BaseModel):
    attribute: str
    audio_path: str
    text_path: str
    status: str

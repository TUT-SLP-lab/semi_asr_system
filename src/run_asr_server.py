from asr_system.view.fastapi_server import app
from dotenv import load_dotenv
from os import getenv
import uvicorn

if __name__ == "__main__":
    load_dotenv()
    HOST = "0.0.0.0"
    PORT = getenv("ASR_SYSTEM_PORT", 5001)

    uvicorn.run(app, host=HOST, port=PORT)

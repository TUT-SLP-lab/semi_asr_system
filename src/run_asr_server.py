from asr_system.view.fastapi_server import app
from common.constant import ASR_SYSTEM_IP, ASR_SYSTEM_PORT

import uvicorn

if __name__ == "__main__":

    uvicorn.run(app, host=ASR_SYSTEM_IP, port=ASR_SYSTEM_PORT)


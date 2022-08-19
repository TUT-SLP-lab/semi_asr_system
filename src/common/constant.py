from dotenv import load_dotenv

import os

load_dotenv()

ASR_SYSTEM_IP = "0.0.0.0"
ASR_SYSTEM_PORT = 5000


DISPATCHER_IP = "0.0.0.0"
DISPATCHER_PORT = 5001

OUTLINE_ACCESS_TOKEN = os.getenv("OUTLINE_ACCESS_TOKEN")
OUTLINE_ADDRESS = "133.15.57.8"
OUTLINE_PORT = 80
OUTLINE_COLLECTION_NAME = "ゼミ"

SPLIT_WAV = "/media/split_wav"
TEXT_OUTPUT = "/mnt/text"

ASR_MODEL_PATH = "/mnt/models/exp/asr_train_asr_transformer_raw_jp_char_sp/valid.acc.ave_10best.pth"
ASR_MODEL_CONFIG = "/mnt/models/exp/asr_train_asr_transformer_raw_jp_char_sp/config.yaml"

LM_MODEL_PATH = "/mnt/models/exp/lm_train_lm_jp_char/40epoch.pth"
LM_MODEL_CONFIG = "/mnt/models/exp/lm_train_lm_jp_char/config.yaml"

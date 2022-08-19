from asr_system.service.asr_inference import ASRInference
from asr_system.service.text_handler import TextHandler

# from asr_system.service.format_text import FormatText
# from asr_system.service.split_audio import SplitAudio

import os
from asr_system.repository.file_io import FileIO
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class Controller:
    def __init__(self) -> None:
        self.asr_inference = ASRInference(
            getenv("ASR_MODEL_CONFIG"), getenv("ASR_MODEL_PATH"), getenv("LM_MODEL_CONFIG"), getenv("LM_MODEL_PATH")
        )
        # self.format_text = FormatText()
        # self.split_audio = SplitAudio()
        self.text_handler = TextHandler()
        self.is_running = False

    def speech2text(self, attribute: str, wav_path: str) -> None:
        """
        Speech to textの機能をすべて包括する関数

        Args:
            attribute(str): 属性名
            wav_path(str): .wav ファイルのパス

        Return:
            None
        """
        self.is_running = True

        # TODO step1 split audio
        split_wav_list = FileIO.get_all_filepath(getenv("SPLIT_WAV"), "*.wav")

        # step2 asr inference
        hyp_list = self.asr_inference.speech2text(split_wav_list)

        # step3 format text

        # step4 wirte and send
        wav_basename = os.path.basename(wav_path)
        self.text_handler.write_text(hyp_list, f"{wav_basename}.txt")
        self.text_handler.send_text_outline(attribute, hyp_list, getenv("OUTLINE_COLLECTION_NAME"))

        # TODO Split 音声を削除

        self.is_running = False

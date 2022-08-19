from asr_system.service.asr_inference import ASRInference
from asr_system.service.text_handler import TextHandler

# from asr_system.service.format_text import FormatText
# from asr_system.service.split_audio import SplitAudio

import os
from common.constant import ASR_MODEL_CONFIG, ASR_MODEL_PATH, LM_MODEL_CONFIG, LM_MODEL_PATH
from common.constant import TEXT_OUTPUT, SPLIT_WAV, COLLECTION_NAME
from asr_system.repository.file_io import FileIO


class Controller:
    def __init__(self) -> None:
        self.asr_inference = ASRInference(ASR_MODEL_CONFIG, ASR_MODEL_PATH, LM_MODEL_CONFIG, LM_MODEL_PATH)
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
        split_wav_list = FileIO.get_all_filepath(SPLIT_WAV, "*.wav")

        # step2 asr inference
        hyp_list = self.asr_inference.speech2text(split_wav_list)

        # step3 format text

        # step4 wirte and send
        wav_basename = os.path.basename(wav_path)
        self.text_handler.write_text(hyp_list, f"{wav_basename}.txt")
        self.text_handler.send_text_outline(attribute, hyp_list, COLLECTION_NAME)

        # TODO Split 音声を削除

        self.is_running = False

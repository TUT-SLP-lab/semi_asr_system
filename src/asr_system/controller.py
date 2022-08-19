from asr_system.service.asr_inference import ASRInference
from asr_system.service.text_handler import TextHandler

# from asr_system.service.format_text import FormatText
from asr_system.service.split_audio import SplitAudio, Sox_Command

import os
import shutil
from asr_system.repository.file_io import FileIO
from os import getenv


class Controller:
    def __init__(self) -> None:
        self.asr_inference = ASRInference(
            getenv("ASR_MODEL_CONFIG"), getenv("ASR_MODEL_PATH"), getenv("LM_MODEL_CONFIG"), getenv("LM_MODEL_PATH")
        )
        # self.format_text = FormatText()
        sox_com = Sox_Command(in_format_op="-V3", out_format_op=None, silence_params=[1, 0.4, 0.2] * 2)
        self.split_audio = SplitAudio(sox_com)
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
        split_wav_dir = getenv("SPLIT_WAV")
        os.mkdir(split_wav_dir)
        try:
            # step1 split audio
            print("Step1 split audio")

            self.split_audio.split(wav_path, os.path.join(split_wav_dir, "output.wav"))
            split_wav_list = FileIO.get_all_filepath(split_wav_dir, "*.wav")
            split_wav_list.sort()
            print(f"wavlit {split_wav_list}")
            # step2 asr inference
            print("Step2 asr inference")
            hyp_list = self.asr_inference.speech2text(split_wav_list)

            # 分割済み音声を削除

            # step3 format text
            print("Step3 format text")

            # step4 wirte and send
            print("Step4 write and send")

            wav_basename = os.path.basename(wav_path)
            self.text_handler.write_text(hyp_list, f"{wav_basename}.txt")
            self.text_handler.send_text_outline(attribute, hyp_list, getenv("OUTLINE_COLLECTION_NAME"))

        except Exception as e:
            print(f"error occored {e}")
        finally:
            # FileIO.delete_all_file(split_wav_dir)
            self.is_running = False

from asr_system.service.asr_inference import ASRInference
from asr_system.service.text_handler import TextHandler, attach_mark
from asr_system.service.split_audio import SplitAudio

import os
import traceback
from asr_system.repository.file_io import FileIO
from os import getenv


class Controller:
    def __init__(self) -> None:
        self.asr_inference = ASRInference(
            getenv("ASR_MODEL_CONFIG"), getenv("ASR_MODEL_PATH"), getenv("LM_MODEL_CONFIG"), getenv("LM_MODEL_PATH")
        )
        self.split_audio = SplitAudio(in_format_op="-V3", out_format_op=None, silence_params=[1, 0.4, 0.2] * 2)
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
        split_wav_base_dir = getenv("SPLIT_WAV")
        os.makedirs(split_wav_base_dir, exist_ok=True)
        try:
            # step1 split audio
            print("Step 1     split audio")

            _, split_wav_dir = self.split_audio.split(wav_path, split_wav_base_dir)
            split_wav_list = FileIO.get_all_filepath(split_wav_dir, "*.wav")
            split_wav_list.sort()
            print(f"wavlit {split_wav_list}")

            self.text_handler.initialize_document(attribute)

            # step2 asr inference
            print("Step 2     asr inference")
            hyp_list = self.asr_inference.speech2texts(split_wav_list)

            print("Step 2.1.1 write raw text")
            wav_basename = os.path.basename(wav_path)
            self.text_handler.write_text(hyp_list, f"{wav_basename}_raw.txt")

            print("Step 2.1.2 send raw text to outline")
            self.text_handler.send_text_list_to_outline(hyp_list)

            print("Step 2.2   add punctuation mark")
            punctuationed_list = attach_mark(hyp_list)

            # step3 wirte and send
            print("Step 3     write text")
            self.text_handler.write_text(punctuationed_list, f"{wav_basename}.txt")

            print("Step 4     send text")
            self.text_handler.final_send_text_outline(punctuationed_list)

            self.text_handler.notify_to_dispatcher(f"{wav_basename}.txt")

        except Exception as e:
            print(traceback.format_exc())
            print(f"error occored {e}")
        finally:
            # FileIO.delete_all_file()
            self.is_running = False

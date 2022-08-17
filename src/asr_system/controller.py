from service.asr_inference import ASRInference
from service.format_text import FormatText
from service.split_audio import SplitAudio
from time import sleep


class Controller:
    def __init__(self) -> None:
        # self.asr_inference = ASRInference
        # self.format_text = FormatText
        # self.split_audio = SplitAudio
        self.is_running = False

    def speech2text(self):
        self.is_running = True

        sleep(10)
        # step1 split audio

        # step2 asr inference

        # step3 format text

        self.is_running = False

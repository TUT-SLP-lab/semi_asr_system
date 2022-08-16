from service.asr_inference import ASRInference
from service.format_text import FormatText
from service.split_audio import SplitAudio


class Controller:
    def __init__(self) -> None:
        self.asr_inference = ASRInference
        self.format_text = FormatText
        self.split_audio = SplitAudio

    def speech2text(self):
        pass

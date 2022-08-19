import espnet2
import soundfile
from espnet2.bin.asr_inference import Speech2Text
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class ASRInference:
    def __init__(self):
        self.s2t = Speech2Text(getenv("ASR_MODEL_CONFIG"), getenv("ASR_MODEL_PATH"))

    def speech2text(self, audio_path: list):
        hyp = []
        for ad in audio_path:
            audio, rate = soundfile.read(ad)
            result = self.s2t(audio)
            hyp.append((result[0])[0])
        return hyp

    def output_file(self, hyp: list, fname: str):
        h = "\n".join(hyp)
        with open(fname, mode="w") as f:
            f.write(h)

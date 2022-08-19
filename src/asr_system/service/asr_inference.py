import espnet2
import soundfile
from espnet2.bin.asr_inference import Speech2Text
from common.constant import ASR_MODEL_CONFIG, ASR_MODEL_PATH, LM_MODEL_CONFIG, LM_MODEL_PATH


class ASRInference:
    def __init__(self):
        self.s2t = Speech2Text(
            asr_train_config=ASR_MODEL_CONFIG,
            asr_model_file=ASR_MODEL_PATH,
            lm_train_config=LM_MODEL_CONFIG,
            lm_file=LM_MODEL_PATH,
        )

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

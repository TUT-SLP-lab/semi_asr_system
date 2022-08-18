import espnet2
import soundfile
from espnet2.bin.asr_inference import Speech2Text

class ASRInference:
    def __init__(self, asr_config: str, asr_model: str, lm_config: str, lm_model: str):
        self.s2t = Speech2Text(asr_train_config=asr_config, asr_model_file=asr_model, lm_train_config=lm_config, lm_file=lm_model)

    def speech2text(self, audio_path: list):
        hyp = []
        for ad in audio_path:
            audio, rate = soundfile.read(ad)
            result = self.s2t(audio)
            hyp.append((result[0])[0])
        return hyp
    
    def output_file(self, hyp: list, fname: str):
        h = '\n'.join(hyp)
        with open(fname, mode='w') as f:
            f.write(h)

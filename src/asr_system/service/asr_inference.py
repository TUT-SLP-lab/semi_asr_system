import espnet2
import soundfile
from espnet2.bin.asr_inference import Speech2Text


class ASRInference:
    def __init__(self, asr_train_config: str, asr_model_file: str, lm_train_config: str, lm_file: str):
        self.s2t = Speech2Text(
            asr_train_config=asr_train_config,
            asr_model_file=asr_model_file,
            lm_train_config=lm_train_config,
            lm_file=lm_file,
        )

    def speech2text(self, audio_path: list):
        hyp = []
        for i, ad in enumerate(audio_path):
            audio, rate = soundfile.read(ad)
            print(f"processing:{i}/{len(audio_path)} sound length :{len(audio)}")
            if len(audio) == 0:
                break
            result = self.s2t(audio)
            hyp.append((result[0])[0])
        return hyp

    def output_file(self, hyp: list, fname: str):
        h = "\n".join(hyp)
        with open(fname, mode="w") as f:
            f.write(h)

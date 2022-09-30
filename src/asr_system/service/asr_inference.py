import espnet2
import soundfile
import resampy
from espnet2.bin.asr_inference import Speech2Text


class ASRInference:
    def __init__(self, asr_train_config: str, asr_model_file: str, lm_train_config: str, lm_file: str):
        self.s2t = Speech2Text(
            asr_train_config=asr_train_config,
            asr_model_file=asr_model_file,
            lm_train_config=lm_train_config,
            lm_file=lm_file,
        )

    def speech2text(self, audio_path: str):
        audio, rate = soundfile.read(audio_path)
        # 2チャンネルの場合、一つに変換
        if audio.ndim == 2:
            audio = audio[:, 0]
        # 長さ0の場合は無視
        if len(audio) == 0:
            return '[emp]'
        else:
            print(f"audio dim{audio.ndim}")
            # 16000kHzに変換
            audio = resampy.resample(audio, rate, 16000)
            print(f"sound length :{len(audio)}")
            result = self.s2t(audio)
            return (result[0])[0]

    def output_file(self, hyp: list, fname: str):
        h = "\n".join(hyp)
        with open(fname, mode="w") as f:
            f.write(h)

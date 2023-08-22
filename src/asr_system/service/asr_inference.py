import torch
import soundfile
import resampy
import nemo.collections.asr as nemo_asr

class ASRInference:
    def __init__(self, asr_train_config: str, asr_model_file: str, lm_train_config: str, lm_file: str):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.s2t = nemo_asr.models.EncDecCTCModel.restore_from(asr_model_file, map_location=device)

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

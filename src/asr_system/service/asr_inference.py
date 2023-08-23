import torch
import soundfile
import subprocess
import nemo.collections.asr as nemo_asr


class ASRInference:
    def __init__(self, asr_train_config: str, asr_model_file: str, lm_train_config: str, lm_file: str):
        device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.s2t = nemo_asr.models.EncDecCTCModel.restore_from(asr_model_file, map_location=device)

    def speech2texts(self, audio_paths: list[str]):
        removed_audio_paths = ASRInference._remove_length_zero_audio(audio_paths)
        result = self.s2t.transcribe(removed_audio_paths,
                                     verbose=True,
                                     batch_size=50,
                                     )
        torch.cuda.empty_cache()
        return result

    def speech2text(self, audio_path: str):
        audio, rate = soundfile.read(audio_path)
        # 長さ0の場合は無視
        if len(audio) == 0:
            return '[emp]'
        else:
            return self.s2t.transcribe([audio_path])[0]

    def output_file(self, hyp: list, fname: str):
        h = "\n".join(hyp)
        with open(fname, mode="w") as f:
            f.write(h)

    def _remove_length_zero_audio(audio_paths: list[str]) -> list[str]:
        return [path
                for path in audio_paths
                if int(subprocess.run(["soxi", "-s", path], capture_output=True, text=True).stdout) != 0]

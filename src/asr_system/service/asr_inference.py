import espnet2
from espnet2.bin.asr_inference import Speech2Text
import soundfile

class ASRInference:
    def __init__(self):
        self.hyp = []

    def speech2text(self, wav_path, config_path, model_path):
        s2t = Speech2Text(config_path, model_path)
        for w in wav_path:
            #print(w)
            audio, rate = soundfile.read(w)
            result = s2t(audio)
            self.hyp.append((result[0])[0])
        return self.hyp
    
    def print_result(self):
        for i in range(len(self.hyp)):
            print('ref:', self.text[i])
            print('hyp:', self.hyp[i])
            print()
    

"""ASR inference スクリプトの単体テスト"""

import sys
import os

sys.path.append(f"/home/hojokeigo/semi_asr_sysystem_2/src/")

print(sys.path)

from asr_system.service.asr_inference import ASRInference

if __name__=="__main__":
    wav_path = ['data/A01M0041_1.wav', 'data/A01M0041_2.wav', 'data/A01M0041_3.wav', 'data/A01M0041_4.wav', 'data/A01M0041_5.wav']
    config_path = 'data/config.yaml'
    model_path = 'data/40epoch.pth'
    file_ = 'test.txt'

    asr = ASRInference()
    hyp = asr.speech2text(wav_path, config_path, model_path)
    print(hyp)
    asr.output_file(file_name)
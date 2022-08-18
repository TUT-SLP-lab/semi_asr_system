"""ASR inference スクリプトの単体テスト"""

import sys
import os
import _path
from asr_system.service.asr_inference import ASRInference

if __name__=="__main__":
    wav_path = ['data/A01M0041_1.wav', 'data/A01M0041_2.wav', 'data/A01M0041_3.wav', 'data/A01M0041_4.wav', 'data/A01M0041_5.wav']
    config_path = 'data/config.yaml'
    model_path = 'data/40epoch.pth'
    file_name = 'test.txt'

    asr = ASRInference(config_path, model_path)
    hyp = asr.speech2text(wav_path)
    print(hyp)
    asr.output_file(hyp, file_name)
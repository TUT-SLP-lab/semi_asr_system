"""ASR inference スクリプトの単体テスト"""

import sys
import os
import _path
from asr_system.service.asr_inference import ASRInference

if __name__=="__main__":
    wav_path = ['data/A01M0041_1.wav', 'data/A01M0041_2.wav', 'data/A01M0041_3.wav', 'data/A01M0041_4.wav', 'data/A01M0041_5.wav']
    asr_config = 'data/config.yaml'
    asr_model = 'data/40epoch.pth'
    lm_config = 'data/config_lm.yaml'
    lm_model = 'data/40epoch_lm.pth'
    file_name = 'test.txt'

    asr = ASRInference(asr_config, asr_model, lm_config, lm_model)
    hyp = asr.speech2text(wav_path)
    print(hyp)
    asr.output_file(hyp, file_name)
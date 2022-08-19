from asr_system.service.split_audio import *
import _path

"""split audioの単体テスト"""
sox_com = Sox_Command(in_format_op="-V3", out_format_op=None, silence_params=[1, 0.2, 0.2] * 2)
saudio = SplitAudio(sox_com)
saudio.split("input.wav", "output.wav")

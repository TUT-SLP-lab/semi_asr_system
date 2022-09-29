import _path
from asr_system.service.split_audio import *
import glob

"""split audioの単体テスト"""
saudio = SplitAudio(in_format_op="-V3", out_format_op=None, silence_params=[1, 0.2, 0.2] * 2)

# 単一の入力ファイルの分割
print(saudio.split("input.wav", "outputs"))

# 複数入力ファイルに対する処理
print(saudio.split(glob.glob("./*.wav"), "out"))

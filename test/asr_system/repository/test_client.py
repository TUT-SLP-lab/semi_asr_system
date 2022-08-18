import sys
import os
import _path

from asr_system.repository.client import OutlineClient
from common.constant import COLLECTION_NAME


outline_clinet = OutlineClient()
status_code, result = outline_clinet.create_document("テストタイトル", "テストテスト・テスト", COLLECTION_NAME)

print(status_code)
print(result)

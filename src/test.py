from os import stat_result
from asr_system.repository.client import OutlineClient
import json
from common.constant import COLLECTION_NAME

outline_clinet = OutlineClient()
status_code, result = outline_clinet.create_document("テストタイトル", "テストテスト・テスト", COLLECTION_NAME)

print(status_code)
print(result)
import sys
import os
import _path

from asr_system.repository.client import OutlineClient
from os import getenv
from dotenv import load_dotenv

load_dotenv()


outline_clinet = OutlineClient()
status_code, result = outline_clinet.create_document("テストタイトル", "テストテスト・テスト", getenv('OUTLINE_COLLECTION_NAME'))

print(status_code)
print(result)

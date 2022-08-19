from asr_system.repository.client import OutlineClient
from asr_system.repository.client import OutlineClient
from asr_system.repository.file_io import FileIO
from common.constant import TEXT_OUTPUT
from typing import List


class TextHandler:
    def __init__(self) -> None:

        self.outline_clinet = OutlineClient()
        self.local_output_path = TEXT_OUTPUT

    def write_text(self, text_list: List, file_name: str):
        file_path = f"{TEXT_OUTPUT}/{file_name}"
        FileIO.output_text_file(text_list, file_path)

    def send_text_outline(self, title: str, text_list: List[str], collection_name: str):
        texts = "\n".join(text_list)
        self.outline_clinet.create_document(title, texts, collection_name)

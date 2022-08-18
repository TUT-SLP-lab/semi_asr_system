from asr_system.repository.client import OutlineClient
from asr_system.repository.client import OutlineClient
from asr_system.repository.file_io import FileIO
from typing import List


class TextHandler:
    def __init__(self, local_output_path, outline_address) -> None:

        self.outline_clinet = OutlineClient()
        self.local_output_path = local_output_path

    def write_text(self, text_list: List, file_name: str):

        FileIO.output_text_file(text_list, file_name)

    def send_text_outline(self, title: str, text_list: List[str], collection_name: str):
        texts = "\n".join(text_list)
        self.outline_clinet.create_document(title, texts, collection_name)

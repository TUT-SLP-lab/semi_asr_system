from asr_system.repository.client import OutlineClient
from asr_system.repository.client import OutlineClient
from asr_system.repository.file_io import FileIO
from typing import List
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class TextHandler:
    def __init__(self) -> None:

        self.outline_clinet = OutlineClient()
        self.local_output_path = getenv("TEXT_OUTPUT")

    def write_text(self, text_list: List, file_name: str):
        file_path = f"{self.local_output_path}/{file_name}"
        FileIO.output_text_file(text_list, file_path)

    def send_text_outline(self, text: str, collection_name: str, title: str=None):
        self.outline_clinet.create_document(title, texts, collection_name)

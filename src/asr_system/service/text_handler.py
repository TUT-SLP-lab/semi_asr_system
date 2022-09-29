from asr_system.repository.client import OutlineClient
from asr_system.repository.client import DispacherClinent
from asr_system.repository.file_io import FileIO
from typing import List
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class TextHandler:
    def __init__(self) -> None:

        self.outline_clinet = OutlineClient()
        self.dispatcher_client = DispacherClinent()
        self.local_output_path = getenv("TEXT_OUTPUT")

    def write_text(self, text_list: List, file_name: str):
        file_path = f"{self.local_output_path}/{file_name}"
        FileIO.output_text_file(text_list, file_path)

<<<<<<< HEAD
    def send_text_outline(self, text: str, collection_name: str, title: str=None):
=======
        # notify to dispatcher api
        self.dispatcher_client.nofity_finish_send_text(file_path)

    def send_text_outline(self, title: str, text_list: List[str], collection_name: str):
        texts = "\n".join(text_list)
>>>>>>> 0b10f85e9b39c8f3fc295e2fa3a283e3939734b7
        self.outline_clinet.create_document(title, texts, collection_name)

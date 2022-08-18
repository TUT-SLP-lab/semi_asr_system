import requests
import json
from typing import Tuple, Dict
from common.constant import (
    OUTLINE_ADDRESS,
    OUTLINE_ACCESS_TOKEN,
    OUTLINE_PORT,
)


class DispacherClinent:
    def __init__(self) -> None:
        pass

    def nofity_finish(self):
        pass

    def send_ASR_text():
        pass


class OutlineClient:
    def __init__(self) -> None:
        self.access_token = OUTLINE_ACCESS_TOKEN
        self.endpoint = f"http://{OUTLINE_ADDRESS}:{OUTLINE_PORT}/api"
        self.headers = {
            "authorization": f"Bearer {self.access_token}",
            "content-type": "application/json",
            "accept": "application/json",
        }

        # JWT token のエラーハンドリング
        status_code, contents = self.confirm_user()
        if status_code != 200:
            raise RuntimeError(contents["message"])

    def confirm_user(self) -> Tuple[int, Dict]:
        """
        get user information from access token

        Args:
        Return:
            int: status code
            json: result contents
        """
        result = requests.post(
            f"{self.endpoint}/auth.info",
            headers=self.headers,
        )

        return result.status_code, json.loads(result.content)

    def collection_list(self) -> Tuple[int, Dict]:
        """
        get collection list

        Args:
        Return:
            int: status code
            json: result contents
        """
        # payload = {"offset": 0, "limit": 10}
        result = requests.post(
            f"{self.endpoint}/collections.list",
            headers=self.headers,  # , data=json.dumps(payload)
        )

        return result.status_code, json.loads(result.content)

    def create_document(self, title: str, text: str, collection_name: str) -> Tuple[int, Dict]:
        """
        create document in Outline

        Args:
            tilte (str): title of document
            text (str): content of document
            collection_name (str): Name of the collection in which to place the document.
        Return:
            int: result code
            Dict: result content
        """
        # get collection id
        _, collection_json = self.collection_list()
        collectionId = self._get_collection_id(collection_json, collection_name)

        # TODO get parent id, Allow the ID of the parent document to be specified.

        payload = {
            "title": title,
            "text": text,
            "collectionId": collectionId,
            # "parentDocumentId": "",
            "publish": True,
        }

        result = requests.post(
            f"{self.endpoint}/documents.create",
            headers=self.headers,
            data=json.dumps(payload),
        )

        return result.status_code, json.loads(result.content)

    @staticmethod
    def _get_collection_id(collection_list: json, collenction_name: str) -> str:
        """
        get collection id in OutLine

        Args:
            collection_list(json): json collection information
            collection_name(str): collection name
        Return:
            str: collection id
        """
        for data in collection_list["data"]:
            if data["name"] == collenction_name:
                return data["id"]

        raise RuntimeError(f"collection name ;{collenction_name} is not exist in OutLine")

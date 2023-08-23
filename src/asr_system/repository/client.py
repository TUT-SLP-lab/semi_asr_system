import requests
import json
from typing import Tuple, Dict, List
from os import getenv
from dotenv import load_dotenv

load_dotenv()


class DispacherClient:
    def __init__(self) -> None:
        self.access_token = getenv("OUTLINE_ACCESS_TOKEN")
        self.endpoint = f"http://{getenv('DISPATCHER_IP')}:{getenv('DISPATCHER_PORT')}/api"
        self.headers = {
            "content-type": "application/json",
            "accept": "application/json",
        }

    def nofity_finish_send_text(self, text_path: str) -> Tuple[int, Dict]:
        payload = {
            "text_path": text_path,
        }

        result = requests.put(
            f"{self.endpoint}/update",
            headers=self.headers,
            data=json.dumps(payload),
        )

        return result.status_code, json.loads(result.content)


class OutlineClient:
    def __init__(self) -> None:
        self.access_token = getenv("OUTLINE_ACCESS_TOKEN")
        self.outline_url = f"http://{getenv('OUTLINE_ADDRESS')}:{getenv('OUTLINE_PORT')}"
        self.endpoint = f"{self.outline_url}/api"
        self.headers = {
            "authorization": f"Bearer {self.access_token}",
            "content-type": "application/json",
            "accept": "application/json",
        }

        # JWT token のエラーハンドリング
        status_code, contents = self.confirm_user()
        if status_code != 200:
            raise RuntimeError(contents["message"])

        self.slack_client = SlackClient()

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

    def get_url_from_id(self, document_id: str) -> str:
        result = requests.post(
            f"{self.endpoint}/documents.info",
            headers=self.headers,
            data=json.dumps({"id": document_id}),
        )
        json_data = json.loads(result.content)
        return f"{self.outline_url}{json_data['data']['url']}"

    def create_document(self, title: str) -> Tuple[int, Dict]:
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

        self.title = title

        payload = {
            "title": title,
            "collectionId": getenv("OUTLINE_COLLECTION_ID"),
            "publish": True,
        }

        result = requests.post(
            f"{self.endpoint}/documents.create",
            headers=self.headers,
            data=json.dumps(payload),
        )

        self.slack_client.send_start_msg(self.title)

        return json.loads(result.content)["data"]["id"]

    def update_document(self, text: str, document_id: str) -> Tuple[int, Dict]:
        payload = {
            "text": text+'\n\n',
            "id": document_id,
            "append": True,
            "publish": True,
        }

        result = requests.post(
            f"{self.endpoint}/documents.update",
            headers=self.headers,
            data=json.dumps(payload),
        )

        return result.status_code, json.loads(result.content)

    def final_update(self, text_list: List[str], document_id: str) -> Tuple[int, Dict]:
        payload = {
            "text": '\n\n'.join(text_list),
            "id": document_id,
            "append": False,
            "publish": True,
        }

        result = requests.post(
            f"{self.endpoint}/documents.update",
            headers=self.headers,
            data=json.dumps(payload),
        )

        outline_url = self.get_url_from_id(document_id)
        self.slack_client.send_finish_msg(self.title, outline_url)

        return result.status_code, json.loads(result.content)


class SlackClient:
    def __init__(self):
        self.endpoint = getenv('SLACK_WEB_HOOK_URL', None)

    def send_msg(self, msg: str) -> None:
        if self.endpoint is not None:
            data = json.dumps({
                "username": "SemiASR",
                "icon_emoji": ":wiki:",
                "text": msg,
            })
            requests.post(self.endpoint, data=data)

    def send_finish_msg(self, attribute: str, outline_url: str) -> None:
        if self.endpoint is not None:
            self.send_msg((
                f"{'_'.join(attribute.split('_')[1:])}"
                "の書き起こしが完了しました。\n"
                f"URL: {outline_url}"
            ))

    def send_start_msg(self, attribute: str) -> None:
        if self.endpoint is not None:
            self.send_msg((
                f"{'_'.join(attribute.split('_')[1:])}"
                "の書き起こしを行っています。"
            ))

import streamlit as st
import subprocess
import dataclasses
import datetime
import os
import time
from pymongo import MongoClient
from bson.objectid import ObjectId
import requests
import shutil
from dotenv import load_dotenv

load_dotenv()


def postQueueServer(post_id: ObjectId) -> None:
    # TODO: get server ip from dotenv
    url = f'http://{os.getenv("DISPATCHER_IP")}:{int(os.getenv("DISPATCHER_PORT"))}/api/id'
    payload = {"id": str(post_id)}
    requests.post(url, json=payload)


def registData(attribute: str, audio_path: str) -> None:
    client = MongoClient(os.getenv("MONGO_DB_IP"), int(os.getenv("MONGO_DB_PORT")))  # TODO: get client info from dotenv
    db = client[os.getenv("MONGO_DB_NAME")]
    collection = db[os.getenv("MONGO_COLLECTION_NAME")]
    post = {
        "attribute": attribute,
        "audio_path": audio_path,
        "text_path": "",
        "status": "unprocessed",
    }
    post_id = collection.insert_one(post).inserted_id
    postQueueServer(post_id)


class Recorder:
    def __init__(self):
        self.record = None
        self.tmpdir = os.path.join(os.path.abspath(os.path.curdir), "record-data")
        self.cmd = "bash recording.sh"
        self.output_dir = os.path.abspath(os.getenv("AUDIO_OUTPUT_DIR"))
        os.makedirs(self.output_dir, exist_ok=True)
        print(self.cmd)

    def start(self, presenter: str):
        if self.record is None:
            self.presenter = presenter
            self.attribute = f"{datetime.date.today()}_{presenter}"
            self.tmp_file_path = os.path.join(self.tmpdir, f"{self.attribute}.wav")
            self.output_file_path = os.path.join(self.output_dir, f"{self.attribute}.wav")

            # subprocessで録音処理を実行
            self.record = subprocess.Popen(f"exec {self.cmd}", stderr=subprocess.PIPE, shell=True)

    def stop(self) -> None:
        if self.record is not None:
            self.record.kill()  # 録音を停止
            (_, stderr) = self.record.communicate()
            if stderr:
                print(stderr)
            # recording.sh内でtmp.wavに音声を書き込んでいるので、
            # 正式な形にrenameする必要がある
            shutil.move(os.path.join(self.tmpdir, "tmp.wav"), self.output_file_path)
            # DBに登録
            registData(attribute=self.attribute, audio_path=self.tmp_file_path)

    def is_alive(self) -> bool:
        return self.record is not None


# ↓ 未処理
@st.experimental_singleton
@dataclasses.dataclass
class ThreadManager:
    recorder = None

    def get_recorder(self) -> object:
        return self.recorder

    def is_running(self) -> bool:
        return self.recorder is not None

    def start_recording(self, presenter: str) -> object:
        if self.recorder is None:
            self.recorder = Recorder()
            self.recorder.start(presenter)
        return self.recorder

    def stop_recording(self) -> None:
        self.recorder.stop()
        del self.recorder
        self.recorder = None


def main():
    st.thread_manager = ThreadManager()

    text_presenter = st.text_input("Presenter", key="presenter", disabled=st.thread_manager.is_running())

    # 録音を制御する部分
    if st.button("Start Recording", disabled=st.thread_manager.is_running()):
        presenter = st.session_state["presenter"]
        recorder = st.thread_manager.start_recording(presenter=presenter)
        st.experimental_rerun()

    if st.button("Stop Recording", disabled=not st.thread_manager.is_running()):
        st.thread_manager.stop_recording()
        st.experimental_rerun()

    if not st.thread_manager.is_running():
        st.markdown("No recorder running.")
    else:
        recorder = st.thread_manager.get_recorder()
        presenter = st.session_state["presenter"]
        st.markdown(f"Presenter: {presenter}")
        placeholder = st.empty()
        if recorder.is_alive():
            placeholder.markdown("Recording")

    # 別セッションでの更新に追従するために、定期的にrerunする
    time.sleep(1)
    st.experimental_rerun()


if __name__ == "__main__":
    main()

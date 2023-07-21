from re import T
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
import webbrowser
from dotenv import load_dotenv

load_dotenv()


def postQueueServer(post_id: ObjectId) -> None:
    # TODO: get server ip from dotenv
    url = f'http://{os.getenv("STREAMLIT_DIPATCHER_IP")}:{int(os.getenv("DISPATCHER_PORT"))}/api/id'
    payload = {"id": str(post_id)}
    requests.post(url, json=payload)


def registData(attribute: str, audio_path: str) -> None:
    DB_USERNAME = os.getenv("MONGO_DB_USERNAME")
    DB_PASSWORD = os.getenv("MONGO_DB_PASSWORD")
    client = MongoClient(
        os.getenv("MONGO_DB_IP"), int(os.getenv("MONGO_DB_PORT")), username=DB_USERNAME, password=DB_PASSWORD
    )  # TODO: get client info from dotenv

    db = client[os.getenv("MONGO_DB_NAME")]
    collection = db[os.getenv("MONGO_COLLECTION_NAME")]
    alter_path = os.getenv("WAV_DIR")
    post = {
        "attribute": attribute,
        "audio_path": os.path.join(alter_path, os.path.basename(audio_path)),
        "text_path": "",
        "status": "unprocessed",
        "add_date": "",
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

    def start(self, presenter: str) -> None:
        if self.record is None:
            self.presenter = presenter
            dt_now = str(datetime.datetime.now()).replace(" ", "T").split(".")[0]
            self.attribute = f"{dt_now}_{presenter}"
            self.tmp_file_path = os.path.join(self.tmpdir, f"{self.attribute}.wav")
            self.output_file_path = os.path.join(self.output_dir, f"{self.attribute}.wav")

            # subprocessで録音処理を実行
            self.record = subprocess.Popen(f"exec {self.cmd} {self.tmp_file_path}", stderr=subprocess.PIPE, shell=True)

    def stop(self) -> None:
        if self.record is not None:
            self.record.kill()  # 録音を停止
            (_, stderr) = self.record.communicate()
            if stderr:
                print(stderr)
            # self.recordの中身を削除
            del self.record
            self.record = None

            # recording.sh内でtmp.wavに音声を書き込んでいるので、
            # 正式な形にrenameする必要がある
            # tmp_path = os.path.join(self.tmpdir, "tmp.wav")
            subprocess.run(
                f"ffmpeg -y -i '{self.tmp_file_path}' -vn -ac 1 -ar 44100 -acodec pcm_s16le -f wav '{self.tmp_file_path}_'", shell=True
            )
            print(f"shutil.move {self.tmp_file_path}_ -> {self.output_file_path}")
            shutil.move(self.tmp_file_path + "_", self.output_file_path)
            # DBに登録
            print(f"regist data: attribute={self.attribute}, audio_path={self.output_file_path}")
            registData(attribute=self.attribute, audio_path=self.output_file_path)

    def is_alive(self) -> bool:
        return self.record is not None


# ↓ 未処理
@st.experimental_singleton
@dataclasses.dataclass
class ThreadManager:
    recorder = None
    presenter = None

    def set_presenter(self, presenter: str) -> None:
        self.presenter = presenter

    def get_presenter(self) -> str:
        if self.presenter is None:
            return ""
        return self.presenter

    def get_recorder(self) -> object:
        return self.recorder

    def is_running(self) -> bool:
        return self.recorder is not None

    def start_recording(self) -> object:
        if self.recorder is None:
            self.recorder = Recorder()
            self.recorder.start(self.presenter)
        return self.recorder

    def stop_recording(self) -> None:
        self.recorder.stop()
        del self.recorder
        self.recorder = None


def main():
    st.thread_manager = ThreadManager()
    MEET_ID = os.getenv("MEET_ID")

    if st.button("Connect Meet"):
        url = f"https://meet.google.com/{MEET_ID}"
        print(url)
        webbrowser.get().open(url)

    if st.thread_manager.get_presenter() != "":
        st.text_input(
            "Presenter", st.thread_manager.get_presenter(), key="presenter", disabled=st.thread_manager.is_running()
        )
    else:
        st.text_input("Presenter", key="presenter", disabled=st.thread_manager.is_running())

    # 録音を制御する部分
    if st.button("Start Recording", disabled=st.thread_manager.is_running()):
        presenter = st.session_state["presenter"]
        st.thread_manager.set_presenter(presenter)
        recorder = st.thread_manager.start_recording()
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
        if recorder is not None:
            placeholder.markdown("Recording")

    # 別セッションでの更新に追従するために、定期的にrerunする
    time.sleep(1)
    st.experimental_rerun()


if __name__ == "__main__":
    main()

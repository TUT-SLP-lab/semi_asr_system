import streamlit as st
import subprocess
import dataclasses
import datetime
import os
import time


class Recorder:
    def __init__(self, presenter: str):
        self.cmd = "parec --format=wav --device=DummyOutput0.monitor"
        self.record = None
        self.basedir = os.path.dirname("record-data")

    def start(self, presenter: str):
        if self.record is None:
            self.presenter = presenter
            self.attribute = f"{datetime.date.today()}_{presenter}"
            self.output_file_path = os.path.join(self.basedir, f"{self.attribute}.wav")
            self.output_file = open(self.output_file_path, "wb")
            self.record = subprocess.Popen(f"exec {self.cmd}", stdout=self.output_file, shell=True)

    def stop(self):
        if self.record is not None:
            self.record.kill()  # 録音を停止
            self.output_file.close()  # ファイルストリームをclose

            # TODO: mongoDBに投げる処理


# ↓ 未処理
@st.experimental_singleton
@dataclasses.dataclass
class ThreadManager:
    recorder = None

    def get_recorder(self):
        return self.recorder

    def is_running(self):
        return self.recorder is not None

    def start_recording(self, presenter: str):
        if self.recorder is not None:
            return self.recorder
        self.recorder = Recorder()
        self.recorder.start(presenter)
        return self.recorder

    def stop_recording(self):
        self.recorder.stop()
        del self.recorder
        self.recorder = None


def main():
    thread_manager = ThreadManager()

    # 録音を制御する部分
    st.text_input("Presenter", key="presenter", disabled=thread_manager.is_running())
    if st.button("Start Recording", disabled=thread_manager.is_running()):
        recorder = thread_manager.start_recording()
        st.experimental_rerun()

    if st.button("Stop Recording", disabled=not thread_manager.is_running()):
        thread_manager.stop_recording()
        st.experimental_rerun()

    if not thread_manager.is_running():
        st.markdown("No recorder running.")
    else:
        recorder = thread_manager.get_recorder()
        presenter = st.session_state["presenter"]
        st.markdown(f"Presenter: {presenter}")
        placeholder = st.empty()
        if recorder.is_alive():
            placeholder.markdown("Recording")

    # 別セッションでの更新に追従するために、定期的にrerunする
    time.sleep(30)
    st.experimental_rerun()


if __name__ == "__main__":
    main()

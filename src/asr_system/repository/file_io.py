from typing import List
import glob
import os


class FileIO:
    @staticmethod
    def read_audio():
        pass

    @staticmethod
    def write_text():
        pass

    @staticmethod
    def get_all_filepath(dir_path: str, pattern: str) -> List[str]:
        """
        パターンにマッチするファイルの絶対パスを取得
        Args:
            pattern(str): サーチするパターン

        Return:
            List: ファイルパスのリスト
        """

        search_str = f"{dir_path}/**/{pattern}"
        path_list = glob.glob(search_str, recursive=True)

        return path_list

    @staticmethod
    def output_text_file(text_list: list, fpath: str):
        """
        改行を含んでfpathで指定されたファイルに書き込む
        """

        h = "\n".join(text_list)
        with open(fpath, mode="w") as f:
            f.write(h)

    @staticmethod
    def delete_all_file():
        """
        target directoryの中のファイルすべてを削除
        """
        for path in glob.glob(f"{os.getenv('SPLIT_WAV')}/*.wav"):
            os.remove(path)

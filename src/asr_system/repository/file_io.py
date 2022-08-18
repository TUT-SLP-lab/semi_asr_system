from typing import List
import glob


class FileIO:
    @staticmethod
    def read_audio(self):
        pass

    @staticmethod
    def write_text(self):
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
    def output_text_file(text_list: list, fname: str):
        h = "\n".join(text_list)
        with open(fname, mode="w") as f:
            f.write(h)

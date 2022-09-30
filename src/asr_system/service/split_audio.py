import os, shutil
import pathlib
import subprocess
from typing import List, overload


class SplitAudio:
    """To generate a sox command that splits the audio file by silence intervals with the specified parameter set."""

    def __init__(
        self,
        in_format_op: str = None,
        out_format_op: str = None,
        silence_params: list = [1, 0.2, 0.2, 1, 0.2, 0.2],
    ):
        if not silence_params == None:
            if not len(silence_params) == 6:
                raise ValueError()

        self.in_format_op = in_format_op
        self.out_format_op = out_format_op
        self.silence_params = silence_params

        self.silence_params = [str(e) for e in self.silence_params]

        self.allowed_type = {
            "iter,iter": ((list, list), (tuple, tuple)),
            "iter,str": ((list, str), (tuple, str)),
            "str,str": ((str, str),),
        }

    def get_command(self, infile: str, outfile: str):
        """return command & arguments as list.

        Args:
            infile (str): sox input file path.
            outfile (str): sox output file path.

        Returns:
            list: command & argument as list.
        """

        cmd = "sox [in_format_op] [infile] [out_format_op] [outfile] silence -l [para0] [para1] [para2]% [para3] [para4] [para5]%: newfile : restart"
        cmd = cmd.split()

        cmd[1] = self.in_format_op
        cmd[2] = infile
        cmd[3] = self.out_format_op
        cmd[4] = outfile
        cmd[7] = self.silence_params[0]
        cmd[8] = self.silence_params[1]
        cmd[9] = self.silence_params[2] + "%"
        cmd[10] = self.silence_params[3]
        cmd[11] = self.silence_params[4]
        cmd[12] = self.silence_params[5] + "%"

        _cmd = []
        for c in cmd:
            if not c == None:
                _cmd.append(c)
        cmd = _cmd

        return cmd

    @overload
    def split(self, infile: List[str], outdir: str = None) -> List[str]:
        """Split input wave-file with specified command set.

        Args:
            infile (List[str]): Input wave-files name
            outdir (str, optional): Output directory name. Defaults to None.

        Raises:
            ValueError: Arguments length is invalid.
            TypeError: Arguments type is invalid.
            Exception: When faild to run sox command for any reasons, exception is raised.

        Returns:
            List[str]: output directories path
        """
        ...

    @overload
    def split(self, infile: List[str], outdir: List[str] = None) -> List[str]:
        """Split input wave-file with specified command set.

        Args:
            infile (List[str]): Input wave-files name
            outdir (List[str], optional): Output directories name. Defaults to None.

        Raises:
            ValueError: Arguments length is invalid.
            TypeError: Arguments type is invalid.
            Exception: When faild to run sox command for any reasons, exception is raised.

        Returns:
            List[str]: output directories path
        """
        ...

    def split(self, infile: str, outdir: str = "/media/split_wav") -> str:
        """Split input wave-file with specified command set.

        Args:
            infile (List[str]): Input wave-files name
            outdir (str, optional): Output directory name. Defaults to '/media/split_wav'.

        Raises:
            ValueError: Arguments length is invalid.
            Exception: When faild to run sox command for any reasons, exception is raised.

        Returns:
            str: output directory path
        """
        infile_type = type(infile)
        outdir_type = type(outdir)
        arg_type = (infile_type, outdir_type)
        print(arg_type, self.allowed_type["str,str"], arg_type in self.allowed_type["str,str"])

        if arg_type in self.allowed_type["iter,iter"]:
            if not len(infile) == len(outdir):
                raise ValueError(
                    "Lenght is diferent infile between outdir : infile {}, outdir {}".format(len(infile), len(outdir))
                )

            out_path = []
            for i, o in zip(infile, outdir):
                out_path.append(self._split(infile=i, outdir=o))

            return out_path
        elif arg_type in self.allowed_type["iter,str"]:
            return self.split(infile, [outdir] * len(infile))
        elif arg_type in self.allowed_type["str,str"]:
            return self._split(infile, outdir)
        else:
            raise TypeError("str and List[str] are allowed in split()")

    def _split(self, infile: str, outdir: str = "/media/split_wav") -> str:
        print(infile)
        print(pathlib.Path(infile).stem)
        outdir = os.path.join(outdir, pathlib.Path(infile).stem)

        if os.path.exists(outdir):
            shutil.rmtree(outdir)
        os.makedirs(outdir)

        out_path = os.path.join(outdir, "out.wav")

        res = subprocess.run(self.get_command(infile, out_path))
        if not res.returncode == 0:
            raise Exception("Faild to run sox command : {}".format(" ".join(self.get_command(infile, outdir))))

        return os.listdir(outdir)

from asr_system.repository.file_io import FileIO
import subprocess


class Sox_Command:
    """For generating arguments for sox command with specified parameter set."""

    def __init__(
        self, in_format_op: str = None, out_format_op: str = None, silence_params: list = [1, 0.2, 0.2, 1, 0.2, 0.2]
    ):
        if not silence_params == None:
            if not len(silence_params) == 6:
                raise ValueError()

        self.in_format_op = in_format_op
        self.out_format_op = out_format_op
        self.silence_params = silence_params

        self.silence_params = [str(e) for e in self.silence_params]

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


class SplitAudio:
    def __init__(self, sox_com: Sox_Command = None):
        if sox_com == None:
            sox_com = Sox_Command(in_format_op="-V3")

        self.sox_com = sox_com

    def split(self, infile, outfile):
        print(self.sox_com.get_command(infile, outfile))
        res = subprocess.call(self.sox_com.get_command(infile, outfile))
        if not res == 0:
            raise Exception("Faild to run sox command : {}".format(self.sox_com.get_command(infile, outfile)))

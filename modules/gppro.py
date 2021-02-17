import subprocess

from modules.config import Paths

class GPPro:

    BIN = "java -jar " + Paths.GPPRO

    def __init__(self, card_name):
        self.card_name = card_name

    def run_info(self):
        cmd_line = self.BIN + " -info > results/" + \
                   self.card_name + "/gp_info.txt"
        try:
            process = subprocess.Popen(cmd_line, shell=True)
            out = process.communicate()[0]
        except Exception as e:
            print(e)
            print(cmd_line)
            return False
        rc = process.returncode
        return rc

from jcpeg.config import Paths
from jcpeg.interfaces import Module, ToolWrapper
from jcpeg.utils import execute_cmd, isfile

INFO_FILE = "/gp_info.txt"
LIST_FILE = "/gp_list.txt"

class GPPro(ToolWrapper):

    BIN = "java -jar " + Paths.GPPRO

    def run_info(self):
        outfile = "results/" + self.card_name + INFO_FILE
        
        if isfile(outfile) and not self.force_mode:
            print("Skipping gp -info.")
            return 0

        print("Running gp -info.")
        cmd_line = self.BIN + " -info > " + outfile
        return execute_cmd(cmd_line)

    def run_list(self):
        outfile = "results/" + self.card_name + LIST_FILE
        
        if isfile(outfile) and not self.force_mode:
            print("Skipping gp -list.")
            return 0

        print("Running gp -list.")
        cmd_line = self.BIN + " -list > " + outfile
        return execute_cmd(cmd_line)

    def parse_info(self):
        filename = "results/" + self.card_name + INFO_FILE

        gpinfo = GPInfo()

        with open(filename, "r") as f:
            lines = f.readlines()

        GPINFO_DISCARD = ["Card Data:", "Card Capabilities:",
                          "More information about your card:",
                          "/parse?ATR"]
            
        i = 0
        while i < len(lines):
                
            line = lines[i].rstrip()
            i += 1
                
            if line.startswith("ATR"):
                gpinfo.atr = line.split(":")[1].strip()
                continue

            if line.startswith("IIN"):
                gpinfo.iin = line.split(":")[1].strip()
                continue

            if line.startswith("CIN"):
                gpinfo.cin = line.split(":")[1].strip()
                continue

            if line.startswith("CPLC"):
                first = line.split(":")[1].strip().split("=")
                gpinfo.cplc[first[0]] = first[1]
                while i < len(lines) and lines[i][0] == " ":
                    pair = lines[i].strip().split("=")
                    gpinfo.cplc[pair[0]] = pair[1]
                    i += 1
                continue

            # ---------------
                
            if line.startswith("Support"):
                gpinfo.supports.append(line)
                continue

            if line.startswith("Version"):
                gpinfo.versions.append(line)
                continue

            if line == "" or any([d in line for d in GPINFO_DISCARD]):
                continue

            gpinfo.other.append(line)

        return gpinfo

    def parse_list(self):

        filename = "results/" + self.card_name + LIST_FILE

        gplist = GPList()

        with open(filename, "r") as f:
            lines = f.readlines()

        i = 0
        while i < len(lines):
                
            line = lines[i].rstrip()
            i += 1

            if line.startswith("ISD"):
                gplist.isd = line.split(":")[1].strip().split(" ")[0]
                continue

            if line.startswith("APP"):
                gplist.app.append(line.split(":")[1].strip().split(" ")[0])
                continue

            if line.startswith("PKG"):
                gplist.pkg.append(line.split(":")[1].strip().split(" ")[0])
                continue

        return gplist

    def run(self):
        self.run_info()
        self.run_list()

    def parse(self):
        modules = []

        modules.append(self.parse_info())
        modules.append(self.parse_list())

        return modules
        
                    

class GPInfo(Module):

    def __init__(self, moduleid="gpinfo"):
        super().__init__(moduleid)
        self.atr = None
        self.cplc = {}
        self.iin = None
        self.cin = None
        self.supports = []
        self.versions = []
        self.other = []


class GPList(Module):

    def __init__(self, moduleid="gplist"):
        super().__init__(moduleid)
        self.isd = None
        self.app = []
        self.pkg = []

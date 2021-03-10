from jcpeg.config import Paths
from jcpeg.interfaces import Module, ToolWrapper
from jcpeg.utils import execute_cmd, isfile

INFO_ARGS = ["-info"]
INFO_FILE = "gp_info.txt"

LIST_ARGS = ["-list"]
LIST_FILE = "gp_list.txt"

class GPPro(ToolWrapper):

    GP_BIN = "java -jar " + Paths.GPPRO

    def run(self, args, outfile):
        outpath = self.get_outfile(outfile)
        cmd_line = self.GP_BIN + " " + " ".join(args) + " > " + outpath
        
        if isfile(outpath) and not self.force_mode:
            print("Skipping " + cmd_line + " (results found).")
            return 0

        print("Running " + cmd_line + ".")
        
        return execute_cmd(cmd_line)


class GPProInfo(GPPro):

    def run(self):
        return super().run(INFO_ARGS, INFO_FILE)
    

    def parse(self):
        filename = self.get_outfile(INFO_FILE)

        gpcplc = GPCPLC()
        gpinfo = GPInfo()
        modules = [gpcplc, gpinfo]

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
                atr = line.split(":")[1].strip()
                modules.insert(0, GPATR(atr=atr))
                continue

            if line.startswith("IIN"):
                gpinfo.iin = line.split(":")[1].strip()
                continue

            if line.startswith("CIN"):
                gpinfo.cin = line.split(":")[1].strip()
                continue

            if line.startswith("CPLC"):
                first = line.split(":")[1].strip().split("=")
                gpcplc.cplc[first[0]] = first[1]
                while i < len(lines) and lines[i][0] == " ":
                    pair = lines[i].strip().split("=")
                    gpcplc.cplc[pair[0]] = pair[1]
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

        return modules


class GPProList(GPPro):

    def run(self):
        return super().run(LIST_ARGS, LIST_FILE)

    def parse(self):

        filename = self.get_outfile(LIST_FILE)

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

        return [gplist]


class GPATR(Module):
    def __init__(self, moduleid="gpatr", atr=None):
        super().__init__(moduleid)
        self.atr = atr


class GPCPLC(Module):
    def __init__(self, moduleid="gpcplc"):
        super().__init__(moduleid)
        self.cplc = {}


class GPInfo(Module):

    def __init__(self, moduleid="gpinfo"):
        super().__init__(moduleid)
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

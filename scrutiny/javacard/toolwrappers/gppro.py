from scrutiny.config import Paths
from scrutiny.interfaces import ToolWrapper
from scrutiny.utils import execute_cmd, isfile
from scrutiny.javacard.modules.gppro import *


INFO_ARGS = ["-info"]
INFO_FILE = "gp_info.txt"

LIST_ARGS = ["-list"]
LIST_FILE = "gp_list.txt"


class GPPro(ToolWrapper):

    GP_BIN = "java -jar " + Paths.GPPRO

    def run(self, args, outfile):
        outpath = self.get_outpath(outfile)
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
        filename = self.get_outpath(INFO_FILE)
        with open(filename, "r") as f:
            lines = f.readlines()

        gpcplc = GPCPLC()
        gpinfo = GPInfo()
        modules = [gpcplc, gpinfo]

        GPINFO_DISCARD = ["Card Data:", "Card Capabilities:",
                          "More information about your card:",
                          "/parse?ATR"]
            
        i = 0
        while i < len(lines):
                
            line = lines[i].rstrip()
            i += 1

            if line == "" or any([d in line for d in GPINFO_DISCARD]):
                continue
                
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
                
            if line.startswith("Support"):
                gpinfo.supports.append(line)
                continue

            if line.startswith("Version"):
                gpinfo.versions.append(line)
                continue

            gpinfo.other.append(line)

        return modules


class GPProList(GPPro):

    def run(self):
        return super().run(LIST_ARGS, LIST_FILE)

    def parse(self):

        filename = self.get_outpath(LIST_FILE)
        with open(filename, "r") as f:
            lines = f.readlines()

        gplist = GPList()

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

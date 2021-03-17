import dominate
from dominate.tags import *

from jcpeg.config import Paths
from jcpeg.interfaces import ContrastModule, Module, ToolWrapper
from jcpeg.utils import execute_cmd, isfile, get_smart_card

INFO_ARGS = ["-info"]
INFO_FILE = "gp_info.txt"

LIST_ARGS = ["-list"]
LIST_FILE = "gp_list.txt"


# Tool Wrappers ---------------------------------------------------------------

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


# Modules ---------------------------------------------------------------------
class GPATRContrast(ContrastModule):

    NAME = "ATR"
    
    def __init__(self,
                 reference_atr, profile_atr,
                 reference_info, profile_info,
                 moduleid="gpatr"):
        super().__init__(moduleid)
        self.reference_atr = reference_atr
        self.profile_atr = profile_atr
        self.reference_info = reference_info
        self.profile_info = profile_info
        
        self.match = self.reference_atr == self.profile_atr

    def __str__(self):
        return self.NAME

    def project_HTML(self):
        
        h3("ATR comparison results")
        p("TODO: insert info text")
        
        h4("ATR:")
        with ul():
            li("Reference ATR: " + self.reference_atr)
            li("Profile ATR: " + self.profile_atr)
        if self.match:
            p("The ATR of tested card matches the reference. "
              "This would suggest the same smart card model.")
        else:
            p("The ATR of tested card does not match the reference. "
              "This would suggest different card models.")

        h4("Additional info from smart card database")
        if self.reference_info:
            p("TODO: Card found text")
            for i in self.reference_info:
                li(i)
        #TODO finish


class GPATR(Module):
    def __init__(self, moduleid="gpatr", atr=None):
        super().__init__(moduleid)
        self.atr = atr

    def contrast(self, other):
        super().contrast(other)

        selfinfo = get_smart_card(self.atr)
        otherinfo = get_smart_card(other.atr)

        cm = GPATRContrast(reference_atr=self.atr,
                           profile_atr=other.atr,
                           reference_info=selfinfo,
                           profile_info=otherinfo)
        return [cm]


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

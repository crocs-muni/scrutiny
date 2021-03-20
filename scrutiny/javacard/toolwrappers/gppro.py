from abc import ABC
from typing import final

from overrides import overrides, EnforceOverrides

from scrutiny.config import Paths
from scrutiny.interfaces import ToolWrapper
from scrutiny.javacard.modules.atr import Atr
from scrutiny.javacard.modules.cplc import Cplc
from scrutiny.utils import execute_cmd, isfile
from scrutiny.javacard.modules.gppro import GPInfo, GPList


INFO_ARGS = ["-info"]
INFO_FILE = "gp_info.txt"

LIST_ARGS = ["-list"]
LIST_FILE = "gp_list.txt"


class GPPro(ToolWrapper, ABC, EnforceOverrides):
    """
    SCRUTINY ToolWrapper for GlobalPlatformPro
    """

    GP_BIN = "java -jar " + Paths.GPPRO

    @final
    def run_gppro(self, args, outfile):
        """
        Wrapper for running GlobalPlatformPro
        """

        outpath = self.get_outpath(outfile)
        cmd_line = self.GP_BIN + " " + " ".join(args) + " > " + outpath

        if isfile(outpath) and not self.force_mode:
            print("Skipping " + cmd_line + " (results found).")
            return 0

        print("Running " + cmd_line + ".")

        return execute_cmd(cmd_line)


class GPProInfo(GPPro):
    """
    SCRUTINY ToolWrapper for GlobalPlatformPro -info
    """

    @overrides
    def run(self):
        return super().run_gppro(INFO_ARGS, INFO_FILE)

    @overrides
    def parse(self):
        filename = self.get_outpath(INFO_FILE)
        with open(filename, "r") as f:
            lines = f.readlines()

        gpcplc = Cplc()
        gpinfo = GPInfo()
        modules = [gpcplc, gpinfo]

        gpinfo_discard = ["Card Data:", "Card Capabilities:",
                          "More information about your card:",
                          "/parse?ATR"]

        i = 0
        while i < len(lines):

            line = lines[i].rstrip()
            i += 1

            if line == "" or any([d in line for d in gpinfo_discard]):
                continue

            if line.startswith("ATR"):
                atr = line.split(":")[1].strip()
                modules.insert(0, Atr(atr=atr))
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
    """
    SCRUTINY ToolWrapper for GlobalPlatformPro -list
    """

    @overrides
    def run(self):
        return super().run_gppro(LIST_ARGS, LIST_FILE)

    @overrides
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

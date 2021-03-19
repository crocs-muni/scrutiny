import os.path
import subprocess

from scrutiny.config import Paths


def isfile(path):
    return os.path.isfile(path)

def isdir(path):
    return os.path.isdir(path)

def errmsg(tool_name, action, e):
    print("Oops!\n"
          "\tSomething went wrong while", action, tool_name + ":\n",
          str(e),
          "\tPlease try again or check the manual set-up section in README.md")
    return False

def execute_cmd(cmd_line):
    try:
        process = subprocess.Popen(cmd_line, shell=True)
        out = process.communicate()[0]
        return process.returncode
    except Exception as e:
        errmsg("'" + cmd_line + "'", "executing", e)
        return 1

def get_smart_card(atr):
    
    with open(Paths.SMARTCARD_LIST, "r", encoding="utf8") as f:
        lines = f.readlines()
        
    info = []
    
    for i in range(len(lines)):
        if atr in lines[i].strip().replace(" ", ""):
            j = 1
            while lines[i+j].startswith("\t"):
                info.append(lines[i+j].strip())
                j += 1

    return info

import os.path
import subprocess


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
    

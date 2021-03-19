import os.path
import subprocess


def isfile(path):
    """
    Convenience alias
    """
    return os.path.isfile(path)


def isdir(path):
    """
    Convenience alias
    """
    return os.path.isdir(path)


def errmsg(tool_name, action, ex):
    """
    Prints error message
    :param tool_name: name of the responsible tool
    :param action: action resulting in exception
    :param ex: exception
    :return: return state
    """
    print("Oops!\n"
          "\tSomething went wrong while", action, tool_name + ":\n",
          str(ex),
          "\tPlease try again or check the manual set-up section in README.md")
    return False


def execute_cmd(cmd_line):
    """
    Executes command
    :param cmd_line: command
    :return: return code of the command
    """
    try:
        process = subprocess.Popen(cmd_line, shell=True)
        _ = process.communicate()[0]
        return process.returncode
    except Exception as e:
        errmsg("'" + cmd_line + "'", "executing", e)
        return 1

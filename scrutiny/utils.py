# MIT License
#
# Copyright (c) 2020-2024 SCRUTINY developers
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

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

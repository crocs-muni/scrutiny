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

from abc import ABC, abstractmethod
from enum import Enum
from typing import final

from overrides import EnforceOverrides

from dominate import tags

class ToolWrapper(ABC, EnforceOverrides):
    """
    SCRUTINY ToolWrapper Interface
    """

    def __init__(self, device_name, force_mode=False):
        self.device_name = device_name
        self.force_mode = force_mode

    def get_outpath(self, filename):
        """
        Returns the path to the tool output
        :param filename: output file name
        :return: path
        """
        return "results/" + self.device_name + "/" + filename

    @abstractmethod
    def run(self):
        """
        Run the wrapped tool
        :return: return code
        """

    @abstractmethod
    def parse(self):
        """
        Parse the results of the wrapped tool and produce modules
        :return: modules
        """


class Module(ABC, EnforceOverrides):
    """
    Scrutiny Module Interface
    """

    def __init__(self, module_name):
        self.module_name = module_name

    @abstractmethod
    def contrast(self, other):
        """
        Produce contras module by comparing self to other module
        :param other: other module of the same type
        :return: list of contrast modules
        """
        if self.module_name != other.module_name:
            raise Exception("Comparing module " + self.module_name +
                            " with " + other.module_name + ".")
        return []

class Contrast(ABC, EnforceOverrides):
    """
    Contrast in-memory representation
    """

    def __init__(self, ref_name, prof_name):
        self.ref_name = ref_name
        self.prof_name = prof_name
        self.result = ContrastState.MATCH
        self.contrasts = []

    def add_contrasts(self, contrasts):
        """
        Add contrasts to the list
        :param contrasts:
        :return:
        """
        self.contrasts.extend(contrasts)


class ContrastModule(ABC, EnforceOverrides):
    """
    SCRUTINY Contrast module
    """

    def __init__(self, module_name):
        self.module_name = module_name
        self.result = None

    def __str__(self):
        return self.module_name

    @final
    def update_result(self):
        """
        Sets current ContrastState to result
        :return: current ContrastState
        """
        self.result = str(self.get_state())
        return self.get_state()

    @abstractmethod
    def get_state(self):
        """
        Get ContrastState according to the module-specific internal state
        :return:
        """

    def project_html_intro(self):
        tags.span(cls="dot " + self.get_state().name.lower())
        tags.h2("Module: " + str(self), style="display: inline-block;")

    @abstractmethod
    def project_html(self, ref_name: str, prof_name: str) -> None:
        """
        Represent contrast using dominate tags
            happens within dominate div tag

        :param ref_name: Reference device name
        :param prof_name: Profile device name
        """

class ContrastState(Enum):
    """
    Contrast State representation
    """
    MATCH, WARN, SUSPICIOUS = range(3)

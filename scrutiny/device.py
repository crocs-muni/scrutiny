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

from enum import Enum

import jsonpickle


class DeviceType(Enum):
    """
    Device Type enum
    """
    JAVA_CARD = "Java Card enabled smart card"


class Device:
    """
    Device in-memory representation
    """

    def __init__(self, name, device_type):
        self.name = name
        self.device_type = device_type
        self.modules = {}

    def add_module(self, module):
        """
        Adds module
        """
        self.modules[module.module_name] = module

    def add_modules(self, modules):
        """
        Adds several modules
        """
        for module in modules:
            self.add_module(module)

    def __str__(self):
        return jsonpickle.encode(self, indent=4)


def load_device(filename: str) -> Device:
    """
    Loads Device object from json file
    :param filename: file name
    :return: Device object
    """
    with open(filename, "r") as f:
        return jsonpickle.decode(f.read())

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

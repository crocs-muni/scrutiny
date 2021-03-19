from enum import Enum


class ToolWrapper(object):
    def __init__(self, device_name, force_mode=False):
        self.device_name = device_name
        self.force_mode = force_mode

    def get_outpath(self, filename):
        return "results/" + self.device_name + "/" + filename

    def run(self):
        pass

    def parse(self):
        pass


class Module(object):

    def __init__(self, module_name):
        self.module_name = module_name

    def contrast(self, other):
        if self.module_name != other.module_name:
            raise Exception("Comparing module " + self.module_name + \
                            " with " + other.module_name + ".")
        return []


class ContrastModule(object):

    def __init__(self, module_name):
        self.module_name = module_name

    def __str__(self):
        return self.module_name
    
    def get_state(self):
        pass

    def project_HTML(self, ref_name=None, prof_name=None):
        pass


class ContrastState(Enum):
    MATCH, WARN, SUSPICIOUS = range(3)

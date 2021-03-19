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
            raise Exception("Comparing module " + self.module_name +
                            " with " + other.module_name + ".")
        return []

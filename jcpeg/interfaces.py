from enum import Enum


class ToolWrapper(object):
    def __init__(self, card_name, force_mode=False):
        self.card_name = card_name
        self.force_mode = force_mode

    def get_outpath(self, filename):
        return "results/" + self.card_name + "/" + filename

    def run(self):
        pass

    def parse(self):
        pass


class Module(object):

    def __init__(self, moduleid):
        self.id = moduleid

    def contrast(self, other):
        if self.id != other.id:
            raise Exception("Comparing module " + self.id + \
                            " with " + other.id + ".")
        return []


class ContrastModule(object):

    def __init__(self, moduleid):
        self.id = moduleid

    def __str__(self):
        return self.moduleid
    
    def get_state(self):
        pass

    def project_HTML(self, ref_name=None, prof_name=None):
        pass


class ContrastState(Enum):
    MATCH, WARN, SUSPICIOUS = range(3)

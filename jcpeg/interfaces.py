class Module(object):

    def __init__(self, moduleid):
        self.id = moduleid

class ToolWrapper(object):
    def __init__(self, card_name, force_mode=False):
        self.card_name = card_name
        self.force_mode = force_mode

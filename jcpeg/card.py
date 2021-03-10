import jsonpickle

class Card(object):

    def __init__(self, name):
        
        self.name = name
        self.atr = None

        self.modules = {}

    def add_module(self, module):
        self.modules[module.id] = module

    def add_modules(self, modules):
        for module in modules:
            self.add_module(module)

    def __str__(self):
        return jsonpickle.encode(self, indent=4)


def load_card(filename):
    with open(filename, "r") as f:
        return jsonpickle.decode(f.read())

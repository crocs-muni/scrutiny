import jsonpickle

class Card(object):

    def __init__(self, name, atr):
        
        self.name = name
        self.atr = atr

        self.modules = {}

    def add_module(self, module):
        self.modules[module.id] = module

    def __str__(self):
        return jsonpickle.encode(self)

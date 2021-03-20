from overrides import overrides

from scrutiny.interfaces import Module


class Cplc(Module):
    """
    SCRUTINY CPLC module
    """
    def __init__(self, module_name="CPLC"):
        super().__init__(module_name)
        self.cplc = {}

    @overrides
    def contrast(self, other):
        return []

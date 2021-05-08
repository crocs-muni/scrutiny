from overrides import overrides

from scrutiny.interfaces import Module, ContrastModule, ContrastState


class Cplc(Module):
    """
    SCRUTINY CPLC module
    """
    def __init__(self, module_name="CPLC"):
        super().__init__(module_name)
        self.cplc = {}

    @overrides
    def contrast(self, other):
        super().contrast(other)

        contrast = CplcContrast()
        contrast.reference = self.cplc
        contrast.profiled = other.cplc

        return [contrast]


class CplcContrast(ContrastModule):
    """
    SCRUTINY CPLC contrast module
    """

    def __init__(self, module_name="CPLC"):
        super().__init__(module_name)
        self.reference = None
        self.profiled = None

    @overrides
    def get_state(self):
        retval = ContrastState.MATCH

        for field in self.reference:

            if field not in self.profiled and retval == ContrastState.MATCH:
                retval = ContrastState.WARN

            if field in self.profiled:
                ref = self.reference[field].split(" ")[0]
                prof = self.profiled[field].split(" ")[0]
                if ref != prof:
                    retval = ContrastState.SUSPICIOUS

        return retval

    @overrides
    def project_html(self, ref_name: str, prof_name: str) -> None:
        pass

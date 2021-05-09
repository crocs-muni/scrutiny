from dominate import tags
from overrides import overrides

from scrutiny.htmlutils import table
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

        for field in self.profiled:

            if field not in self.reference and retval == ContrastState.MATCH:
                retval = ContrastState.WARN

        return retval

    @overrides
    def project_html(self, ref_name: str, prof_name: str) -> None:
        tags.h3("CPLC comparison results")
        tags.p("This module compares CPLC of smart cards. "
               "Bear in mind that the CPLC data is static and could be faked. "
               "Therefore, matching result does not guarantee match. "
               "However, mismatch in CPLC data is highly suspicious.")

        tags.h4("CPLC:")

        if self.get_state() == ContrastState.MATCH:
            tags.p("CPLC data seems to match between cards.")
        elif self.get_state() == ContrastState.WARN:
            tags.p("There are missing CPLC fields in results for one of the "
                   "cards. This could be due to error in measurement, but "
                   "it could suggest suspicious difference.")
        else:
            tags.p("There are differences in CPLC fields. The cards probably "
                   "don't match, or differ in hardware or software revision.")

        self.output_table(ref_name, prof_name)

    def output_table(self, ref_name: str, prof_name: str):
        """Output CPLC comparison table"""

        header = ["CPLC Field",
                  ref_name + " (reference)",
                  prof_name + " (profiled)"]

        data = []
        keys = set()
        keys.update(self.reference.keys())
        keys.update(self.profiled.keys())

        for key in keys:
            ref = self.reference[key] if key in self.reference else "Missing"
            prof = self.profiled[key] if key in self.profiled else "Missing"
            data.append([key, ref, prof])

        table(data, header,
              red_predicate=lambda line:
              line[1].split(" ")[0] != line[2].split(" ")[0])

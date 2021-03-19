from dominate import tags

from scrutiny.contrast import ContrastModule, ContrastState
from scrutiny.interfaces import Module
from scrutiny.javacard.utils import find_atr_in_database


class Atr(Module):
    def __init__(self, module_name="ATR", atr=None):
        super().__init__(module_name)
        self.atr = atr

    def contrast(self, other):
        super().contrast(other)

        selfinfo = find_atr_in_database(self.atr)
        otherinfo = find_atr_in_database(other.atr)

        cm = AtrContrast(ref_atr=self.atr,
                         prof_atr=other.atr,
                         ref_info=selfinfo,
                         prof_info=otherinfo)
        return [cm]


class AtrContrast(ContrastModule):

    def __init__(self,
                 ref_atr, prof_atr,
                 ref_info, prof_info,
                 module_name="ATR"):

        super().__init__(module_name)
        self.ref_atr = ref_atr
        self.prof_atr = prof_atr
        self.ref_info = ref_info
        self.prof_info = prof_info

        self.match = self.ref_atr == self.prof_atr

    def get_state(self):
        if self.match:
            return ContrastState.MATCH
        return ContrastState.SUSPICIOUS

    def project_html(self, ref_name, prof_name):

        tags.h3("ATR comparison results")
        tags.p("This module compares ATR of the smart cards and searches database "
               "of known smart cards for additional information.")

        tags.h4("ATR:")
        with tags.table():
            with tags.tr():
                tags.td("Reference ATR (" + ref_name + ")")
                tags.td(self.ref_atr)
            with tags.tr():
                tags.td("Profile ATR (" + prof_name + ")")
                tags.td(self.prof_atr)

        if self.match:
            tags.p("The ATR of tested card matches the reference. "
                   "This would suggest the same smart card model.")
        else:
            tags.p("The ATR of tested card does not match the reference. "
                   "This would suggest different smart card models.")

        tags.h4("Additional info from smart card database")
        if self.ref_info:
            tags.p("The reference card (" + ref_name + ") was found in the database:")
            with tags.div():
                for i in self.ref_info:
                    tags.p(i)
        else:
            tags.p("The reference card (" + ref_name + ") was not found in the database.")
        if self.prof_info:
            tags.p("The profiled card (" + prof_name + ") was found in the database:")
            with tags.div():
                for i in self.prof_info:
                    tags.p(i)
        else:
            tags.p("The profiled card (" + prof_name + " was not found in the database.")

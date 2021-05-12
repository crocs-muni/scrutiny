from dominate import tags
from overrides import overrides

from scrutiny import config
from scrutiny.interfaces import Module, ContrastModule, ContrastState
from scrutiny.javacard.utils import find_atr_in_database


class Atr(Module):
    """
    SCRUTINY ATR module
    """

    def __init__(self, module_name="ATR", atr=None):
        super().__init__(module_name)
        self.atr = atr

    @overrides
    def contrast(self, other):
        super().contrast(other)

        self_info = find_atr_in_database(self.atr)
        other_info = find_atr_in_database(other.atr)

        cm = AtrContrast()

        cm.ref_atr = self.atr
        cm.prof_atr = other.atr
        cm.ref_info = self_info
        cm.prof_info = other_info

        return [cm]


class AtrContrast(ContrastModule):
    """
    SCRUTINY ATR contrast module
    """

    def __init__(self, module_name="ATR"):

        super().__init__(module_name)
        self.ref_atr = None
        self.prof_atr = None
        self.ref_info = None
        self.prof_info = None

    @overrides
    def get_state(self):
        if self.ref_atr == self.prof_atr:
            return ContrastState.MATCH
        return ContrastState.SUSPICIOUS

    @overrides
    def project_html(self, ref_name, prof_name):

        tags.h3("ATR comparison results")
        tags.p("This module compares ATR of the smart cards "
               "and searches database of known smart cards "
               "for additional information.")

        tags.h4("ATR:")
        with tags.table():
            with tags.tr():
                tags.td("Reference ATR (" + ref_name + ")")
                tags.td(self.ref_atr)
            with tags.tr():
                tags.td("Profile ATR (" + prof_name + ")")
                tags.td(self.prof_atr)

        if self.ref_atr == self.prof_atr:
            tags.p("The ATR of tested card matches the reference. "
                   "This would suggest the same smart card model.")
        else:
            tags.p("The ATR of tested card does not match the reference. "
                   "This would suggest different smart card models.")

        tags.h4("Additional info from smart card database")

        tags.p("This information was taken from database of known "
               "smart cards, distributed under GNU GPLv2.")
        tags.p("For complete list, check:")
        tags.a(config.URL.SMARTCARD_LIST,
               href=config.URL.SMARTCARD_LIST)

        if self.ref_info:
            tags.p("The reference card (" + ref_name +
                   ") was found in the database:")
            with tags.div():
                for i in self.ref_info:
                    tags.p(i)
        else:
            tags.p("The reference card (" + ref_name +
                   ") was not found in the database.")
        if self.prof_info:
            tags.p("The profiled card (" + prof_name +
                   ") was found in the database:")
            with tags.div():
                for i in self.prof_info:
                    tags.p(i)
        else:
            tags.p("The profiled card (" + prof_name +
                   ") was not found in the database.")

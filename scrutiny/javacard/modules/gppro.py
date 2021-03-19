import dominate
from dominate.tags import *

from scrutiny.interfaces import ContrastModule, Module, ContrastState
from scrutiny.utils import get_smart_card


class GPATR(Module):
    def __init__(self, moduleid="gpatr", atr=None):
        super().__init__(moduleid)
        self.atr = atr

    def contrast(self, other):
        super().contrast(other)

        selfinfo = get_smart_card(self.atr)
        otherinfo = get_smart_card(other.atr)

        cm = GPATRContrast(ref_atr=self.atr,
                           prof_atr=other.atr,
                           ref_info=selfinfo,
                           prof_info=otherinfo)
        return [cm]


class GPATRContrast(ContrastModule):

    NAME = "ATR"
    
    def __init__(self,
                 ref_atr, prof_atr,
                 ref_info, prof_info,
                 moduleid="gpatr"):

        super().__init__(moduleid)
        self.ref_atr = ref_atr
        self.prof_atr = prof_atr
        self.ref_info = ref_info
        self.prof_info = prof_info
        
        self.match = self.ref_atr == self.prof_atr

    def __str__(self):
        return self.NAME
    
    def get_state(self):
        if self.match:
            return ContrastState.MATCH
        return ContrastState.SUSPICIOUS

    def project_HTML(self, ref_name, prof_name):
        
        h3("ATR comparison results")
        p("This module copares ATR of the smart cards and serches database "
        "of known smart cards for additional information.")
        
        h4("ATR:")
        with table():
            with tr():
                td("Reference ATR (" + ref_name + ")")
                td(self.ref_atr)
            with tr():
                td("Profile ATR (" + prof_name + ")")
                td(self.prof_atr)
            
        if self.match:
            p("The ATR of tested card matches the reference. "
              "This would suggest the same smart card model.")
        else:
            p("The ATR of tested card does not match the reference. "
              "This would suggest different smart card models.")

        h4("Additional info from smart card database")
        if self.ref_info:
            p("The reference card (" + ref_name + ") was found in the database:")
            with div():
                for i in self.ref_info:
                    p(i)
        else:
            p("The reference card (" + ref_name + ") was not found in the database.")
        if self.prof_info:
            p("The profiled card (" + prof_name + ") was found in the database:")
            with div():
                for i in self.prof_info:
                    p(i)
        else:
            p("The profiled card (" + prof_name + " was not found in the database.")


class GPCPLC(Module):
    def __init__(self, moduleid="gpcplc"):
        super().__init__(moduleid)
        self.cplc = {}


class GPInfo(Module):

    def __init__(self, moduleid="gpinfo"):
        super().__init__(moduleid)
        self.iin = None
        self.cin = None
        self.supports = []
        self.versions = []
        self.other = []


class GPList(Module):

    def __init__(self, moduleid="gplist"):
        super().__init__(moduleid)
        self.isd = None
        self.app = []
        self.pkg = []

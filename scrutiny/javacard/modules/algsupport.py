from dominate.tags import *

from scrutiny.interfaces import Module
from scrutiny.contrast import ContrastModule, ContrastState


class AlgSupport(Module):
    def __init__(self, module_name="Algorithm Support"):
        super().__init__(module_name)
        self.test_info = {}
        self.jcsystem = {}
        self.cplc = {}
        self.support = {}
    
    def contrast(self, other):

        matching = []
        differences = []
        suspicions = []

        for key in self.support.keys():

            if key not in other.support.keys():
                differences.append((key, True, False))
                break

            ref = self.support[key]
            prof = other.support[key]

            if ref[0] == prof[0]:
                matching.append((key, ref, prof))
            else:
                suspicions.append((key, ref, prof))
        
        for key in other.support.keys():
            if key not in self.support.keys():
                differences.append((key, False, True))
        
        return [AlgSupportContrast(matching, differences, suspicions)]


class AlgSupportContrast(ContrastModule):

    def __init__(self, matching, differences, suspicions, module_name="Algorithm Support"):
        super().__init__(module_name)
        self.matching = matching
        self.differences = differences
        self.suspicions = suspicions
    
    def get_state(self):
        if self.suspicions:
            return ContrastState.SUSPICIOUS
        if self.differences:
            return ContrastState.WARN
        return ContrastState.MATCH
    
    def project_html(self, ref_name, prof_name):
        
        h3("Algorithm Support comparison results")
        p("This module compares Java Card algorithm support between the cards.")
        
        h4("Overview:")
            
        p(
            "The cards match in " + str(len(self.matching)) + " algorithms."
        )
        p(
            "There are " + str(len(self.differences)) + " algorithms with missing "
            "results for either card."
        )
        p(
            "There are " + str(len(self.suspicions)) + " algorithms with different "
            "results for either card."
        )

        if self.suspicions:
            h4("Differences in algorithm support:", style="color:var(--red-color)")
            with table():
                with th("Algorithm"):
                    td("Reference card (" + ref_name + ")")
                    td("Profiled card (" + prof_name + ")")
                for suspicion in self.suspicions:
                    key, ref, prof = suspicion
                    with tr():
                        td(key)
                        td("Yes") if ref[0] else td("No")
                        td("Yes") if prof[0] else td("No")

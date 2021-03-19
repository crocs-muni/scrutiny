from typing import Optional, Dict, Tuple, List

from dominate.tags import *

from scrutiny.interfaces import Module
from scrutiny.contrast import ContrastModule, ContrastState


class SupportResult(object):

    def __init__(
            self,
            support: Optional[bool] = None,
            time_elapsed: Optional[float] = None,
            persistent_memory: Optional[int] = None,
            ram_deselect: Optional[int] = None,
            ram_reset: Optional[int] = None
    ) -> None:
        self.support = support
        self.time_elapsed = time_elapsed
        self.persistent_memory = persistent_memory
        self.ram_deselect = ram_deselect
        self.ram_reset = ram_reset


class AlgSupport(Module):

    def __init__(self, module_name="Algorithm Support"):
        super().__init__(module_name)
        self.test_info = {}
        self.jcsystem = {}
        self.apdu = {}
        self.cplc = {}
        self.support: Dict[str, SupportResult] = {}

    def contrast(self, other):

        matching: Dict[str, List[SupportResult]] = {}
        differences: Dict[str, List[Optional[SupportResult]]] = {}
        suspicions: Dict[str, List[SupportResult]] = {}

        for key in self.support.keys():

            if key not in other.support.keys():
                differences[key] = [self.support[key], None]
                break

            ref: SupportResult = self.support[key]
            prof: SupportResult = other.support[key]

            if ref.support == prof.support:
                matching[key] = [ref, prof]
            else:
                suspicions[key] = [ref, prof]

        for key in other.support.keys():
            if key not in self.support.keys():
                differences[key] = [None, other.support[key]]

        return [AlgSupportContrast(matching, differences, suspicions)]


class AlgSupportContrast(ContrastModule):

    def __init__(self, matching, differences, suspicions, module_name="Algorithm Support"):
        super().__init__(module_name)
        self.matching: Dict[str, List[SupportResult]] = matching
        self.differences: Dict[str, List[Optional[SupportResult]]] = differences
        self.suspicions: Dict[str, List[SupportResult]] = suspicions

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
                for key in self.suspicions.keys():
                    ref = self.suspicions[key][0]
                    prof = self.suspicions[key][1]
                    with tr():
                        td(key)
                        td("Yes") if ref.support else td("No")
                        td("Yes") if prof.support else td("No")

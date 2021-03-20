from typing import Optional, Dict, List

from dominate import tags

from scrutiny.contrast import ContrastModule, ContrastState
from scrutiny.javacard.modules.jcalgtest import JCAlgTestModule


class SupportResult:
    """
    Class to store results of algorithm support testing
    """

    def __init__(self) -> None:
        self.support: Optional[bool] = None
        self.time_elapsed: Optional[float] = None
        self.persistent_memory: Optional[int] = None
        self.ram_deselect: Optional[int] = None
        self.ram_reset: Optional[int] = None


class AlgSupport(JCAlgTestModule):
    """
    Scrutiny algorithm support module
    """

    def __init__(self, module_name="Algorithm Support"):
        super().__init__(module_name)
        self.support: Dict[str, SupportResult] = {}

    def contrast(self, other):

        matching: Dict[str, List[SupportResult]] = {}
        differences: Dict[str, List[Optional[SupportResult]]] = {}
        suspicions: Dict[str, List[SupportResult]] = {}

        for key in self.support:

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
    """
    Scrutiny algorithm support contrast module
    """

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

        tags.h3("Algorithm Support comparison results")
        tags.p("This module compares Java Card algorithm support between the cards.")

        tags.h4("Overview:")

        tags.p(
            "The cards match in " + str(len(self.matching)) + " algorithms."
        )
        tags.p(
            "There are " + str(len(self.differences)) + " algorithms with missing "
            "results for either card."
        )
        tags.p(
            "There are " + str(len(self.suspicions)) + " algorithms with different "
            "results for either card."
        )

        if self.suspicions:
            tags.h4("Differences in algorithm support:", style="color:var(--red-color)")
            with tags.table():
                with tags.th("Algorithm"):
                    tags.td("Reference card (" + ref_name + ")")
                    tags.td("Profiled card (" + prof_name + ")")
                for key in self.suspicions.keys():
                    ref = self.suspicions[key][0]
                    prof = self.suspicions[key][1]
                    with tags.tr():
                        tags.td(key)
                        tags.td("Yes" if ref.support else "No")
                        tags.td("Yes" if prof.support else "No")

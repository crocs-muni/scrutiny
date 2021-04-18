from typing import Optional, Dict, List

from dominate import tags
from overrides import overrides

from scrutiny.htmlutils import table
from scrutiny.interfaces import ContrastModule, ContrastState
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

    @overrides
    def add_result(self, key: str, result: SupportResult) -> None:
        self.support[key] = result

    def __init__(self, module_name="Algorithm Support"):
        super().__init__(module_name)
        self.support: Dict[str, SupportResult] = {}

    @overrides
    def contrast(self, other):

        matching: Dict[str, List[SupportResult]] = {}
        differences: Dict[str, List[Optional[SupportResult]]] = {}
        support_mismatch: Dict[str, List[SupportResult]] = {}

        for key in self.support:

            if key not in other.support.keys():
                differences[key] = [self.support[key], None]
                break

            ref: SupportResult = self.support[key]
            prof: SupportResult = other.support[key]

            if ref.support == prof.support:
                matching[key] = [ref, prof]
            else:
                support_mismatch[key] = [ref, prof]

        for key in other.support.keys():
            if key not in self.support.keys():
                differences[key] = [None, other.support[key]]

        contrast = AlgSupportContrast()
        contrast.matching = matching
        contrast.different = differences
        contrast.support_mismatch = support_mismatch

        return [contrast]


class AlgSupportContrast(ContrastModule):
    """
    Scrutiny algorithm support contrast module
    """

    def __init__(self, module_name="Algorithm Support"):
        super().__init__(module_name)
        self.matching: Dict[str, List[SupportResult]] = {}
        self.different: Dict[str, List[Optional[SupportResult]]] = {}
        self.support_mismatch: Dict[str, List[SupportResult]] = {}

    @overrides
    def get_state(self):
        if self.support_mismatch:
            return ContrastState.SUSPICIOUS
        if self.different:
            return ContrastState.WARN
        return ContrastState.MATCH

    @overrides
    def project_html(self, ref_name, prof_name):

        self.output_intro()

        if self.support_mismatch:
            self.output_support_mismatch(prof_name, ref_name)

    def output_intro(self):
        """Output introductory section"""

        tags.h3("Algorithm Support comparison results")
        tags.p("This module compares Java Card "
               "algorithm support between the cards.")
        tags.h4("Overview:")
        tags.p(
            "The cards match in " + str(len(self.matching)) + " algorithms."
        )
        tags.p(
            "There are " + str(len(self.different)) +
            " algorithms with missing "
            "results for either card."
        )
        tags.p(
            "There are " + str(len(self.support_mismatch)) +
            " algorithms with different "
            "results for either card."
        )

    def output_support_mismatch(self, prof_name, ref_name):
        """Output suspicions section"""

        tags.h4("Differences in algorithm support:",
                style="color:var(--red-color)")

        header = ["Algorithm",
                  ref_name + " (reference)",
                  prof_name + " (profiled)"]

        data = []
        for key in self.support_mismatch.keys():
            ref = self.support_mismatch[key][0]
            prof = self.support_mismatch[key][1]
            data.append([key,
                         "Yes" if ref.support else "No",
                         "Yes" if prof.support else "No"])

        table(data, header)

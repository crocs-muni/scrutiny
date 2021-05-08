from typing import Optional, Dict, List

from dominate import tags
from overrides import overrides

from scrutiny.htmlutils import table, show_hide_div
from scrutiny.interfaces import ContrastModule, ContrastState
from scrutiny.javacard.modules.jcalgtest import JCAlgTestModule, SupportResult


class AlgSupport(JCAlgTestModule):
    """
    Scrutiny algorithm support module
    """

    MEMORY_DIFFERENCE_THRESHOLD = 16

    @overrides
    def add_result(self, key: str, result: SupportResult) -> None:
        self.support[key] = result

    def __init__(self, module_name="Algorithm Support"):
        super().__init__(module_name)
        self.support: Dict[str, SupportResult] = {}

    @overrides
    def contrast(self, other):
        super().contrast(other)

        matching: Dict[str, List[SupportResult]] = {}
        missing: Dict[str, List[Optional[SupportResult]]] = {}
        support_mismatch: Dict[str, List[SupportResult]] = {}
        memory_mismatch: Dict[str, List[SupportResult]] = {}
        reset_mismatch: Dict[str, List[SupportResult]] = {}
        deselect_mismatch: Dict[str, List[SupportResult]] = {}

        for key in self.support:

            if key not in other.support.keys():
                missing[key] = [self.support[key], None]
                continue

            ref: SupportResult = self.support[key]
            prof: SupportResult = other.support[key]

            if ref.support != prof.support:
                support_mismatch[key] = [ref, prof]
                continue

            matches = True
            mdt = self.MEMORY_DIFFERENCE_THRESHOLD

            if ref.persistent_memory and prof.persistent_memory and \
                    abs(ref.persistent_memory - prof.persistent_memory) > mdt:
                memory_mismatch[key] = [ref, prof]
                matches = False

            if ref.ram_reset and prof.ram_reset and \
                    abs(ref.ram_reset - prof.ram_reset) > mdt:
                reset_mismatch[key] = [ref, prof]
                matches = False

            if ref.ram_deselect and prof.ram_deselect and \
                    abs(ref.ram_deselect - prof.ram_deselect) > mdt:
                deselect_mismatch[key] = [ref, prof]
                matches = False

            if matches:
                matching[key] = [ref, prof]

        for key in other.support.keys():
            if key not in self.support.keys():
                missing[key] = [None, other.support[key]]

        contrast = AlgSupportContrast()
        contrast.matching = matching
        contrast.missing = missing
        contrast.support_mismatch = support_mismatch
        contrast.memory_mismatch = memory_mismatch
        contrast.reset_mismatch = reset_mismatch
        contrast.deselect_mismatch = deselect_mismatch

        return [contrast]


class AlgSupportContrast(ContrastModule):
    """
    Scrutiny algorithm support contrast module
    """

    def __init__(self, module_name="Algorithm Support"):
        super().__init__(module_name)
        self.matching: Dict[str, List[SupportResult]] = {}
        self.missing: Dict[str, List[Optional[SupportResult]]] = {}
        self.support_mismatch: Dict[str, List[SupportResult]] = {}
        self.memory_mismatch: Dict[str, List[SupportResult]] = {}
        self.reset_mismatch: Dict[str, List[SupportResult]] = {}
        self.deselect_mismatch: Dict[str, List[SupportResult]] = {}

    @overrides
    def get_state(self):
        if self.support_mismatch:
            return ContrastState.SUSPICIOUS
        if self.missing or self.memory_mismatch or self.reset_mismatch \
                or self.deselect_mismatch:
            return ContrastState.WARN
        return ContrastState.MATCH

    @overrides
    def project_html(self, ref_name, prof_name):

        self.output_intro()

        if self.support_mismatch:
            self.output_support_mismatch(ref_name, prof_name)

        mem_mismatch = len(self.memory_mismatch) + len(self.reset_mismatch) \
            + len(self.deselect_mismatch)

        if mem_mismatch > 0:
            self.output_memory_mismatch(ref_name, prof_name)

        if self.missing:
            self.output_missing(ref_name, prof_name)

        self.output_matching(ref_name, prof_name)

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
            "There are " + str(len(self.missing)) +
            " algorithms with missing results for either card."
        )
        tags.p(
            "There are " + str(len(self.support_mismatch)) +
            " algorithms with different results."
        )
        mem_mismatch = len(self.memory_mismatch) + len(self.reset_mismatch) \
            + len(self.deselect_mismatch)
        tags.p(
            "There are " + str(mem_mismatch) +
            " algorithms with suspicious differences in memory allocation."
        )

    def output_support_mismatch(self, ref_name: str, prof_name: str):
        """Output algorithm support differences section"""

        tags.h4("Differences in algorithm support:",
                style="color:var(--red-color);display:inline-block")

        header = ["Algorithm",
                  ref_name + " (reference)",
                  prof_name + " (profiled)"]

        data = []
        for key in self.support_mismatch:
            ref = self.support_mismatch[key][0]
            prof = self.support_mismatch[key][1]
            data.append([key,
                         "Supported" if ref.support else "Unsupported",
                         "Supported" if prof.support else "Unsupported"])

        sm_div = show_hide_div("support_mismatch_div")

        with sm_div:
            tags.p(
                "If an algorithm is supported by the reference card, but not "
                "the profiled card and vice versa, the cards almost certainly "
                "do not match.")
            table(data, header,
                  green_value="Supported",
                  red_value="Unsupported")

    def output_memory_mismatch(self, ref_name: str, prof_name: str):
        """Output memory mismatch section"""

        tags.h4("Differences in memory allocation during tests:",
                style="color:var(--orange-color);display:inline-block")

        sm_div = show_hide_div("support_memory_mismatch_div", hide=True)

        with sm_div:
            tags.p("Differences in bytes of allocated memory above "
                   "certain threshold might be suspicious, as the memory "
                   "allocated during the test of the same algorithm should "
                   "remain similar.")

            for dataset in [self.memory_mismatch,
                            self.reset_mismatch,
                            self.deselect_mismatch]:
                if dataset:
                    self.output_single_memory_mismatch(ref_name, prof_name,
                                                       dataset)

    def output_single_memory_mismatch(self, ref_name: str, prof_name: str,
                                      dataset: Dict[str, List[SupportResult]]):
        """Output part of memory mismatch section"""

        mismatch = ""
        if dataset is self.memory_mismatch:
            mismatch = "persistent memory allocation"
        elif dataset is self.reset_mismatch:
            mismatch = "memory allocation during reset call"
        elif dataset is self.deselect_mismatch:
            mismatch = "memory allocation during deselect call"
        tags.h4("Differences in " + mismatch + ":",
                style="color:var(--orange-color)")

        header = ["Algorithm",
                  ref_name + " (reference)",
                  prof_name + " (profiled)"]

        data = []
        for key in dataset.keys():
            if dataset is self.memory_mismatch:
                ref = str(dataset[key][0].persistent_memory)
                prof = str(dataset[key][1].persistent_memory)
            elif dataset is self.reset_mismatch:
                ref = str(dataset[key][0].ram_reset)
                prof = str(dataset[key][1].ram_reset)
            elif dataset is self.deselect_mismatch:
                ref = str(dataset[key][0].ram_deselect)
                prof = str(dataset[key][1].ram_deselect)
            else:
                raise Exception("Wrong parameter in output_memory_mismatch")
            data.append([key, ref, prof])

        table(data, header)

    def output_missing(self, ref_name, prof_name):
        """Output missing measurements section"""

        tags.h4("Missing measurements in algorithm support:",
                style="color:var(--yellow-color);display:inline-block")

        header = ["Algorithm",
                  ref_name + " (reference)",
                  prof_name + " (profiled)"]

        data = []
        for key in self.missing:
            ref = self.missing[key][0]
            prof = self.missing[key][1]

            if ref:
                ref = "Supported" if ref.support else "Unsupported"
            else:
                ref = "Result missing"
            if prof:
                prof = "Supported" if prof.support else "Unsupported"
            else:
                prof = "Result missing"

            data.append([key, ref, prof])

        sm_div = show_hide_div("support_missing_div", hide=True)

        with sm_div:
            tags.p(
                "These are the algorithms which had their results missing on "
                "one of the cards. These should be checked manually."
            )
            table(data, header,
                  green_value="Supported",
                  red_value="Unsupported")

    def output_matching(self, ref_name, prof_name):
        """Output matching section"""

        tags.h4("List of algorithms with matching results:",
                style="color:var(--green-color);display:inline-block")

        header = ["Algorithm",
                  ref_name + " (reference)",
                  prof_name + " (profiled)"]

        data = []
        for key in self.matching:
            ref = self.matching[key][0]
            prof = self.matching[key][1]
            data.append([key,
                         "Supported" if ref.support else "Unsupported",
                         "Supported" if prof.support else "Unsupported"])

        sm_div = show_hide_div("support_matching_div", hide=True)

        with sm_div:
            tags.p(
                "These are the algorithms which had their results matching "
                "between cards with no significant differences in the memory "
                "allocation."
            )
            table(data, header,
                  green_value="Supported",
                  red_value="Unsupported")

from typing import Dict, List, Optional

from dominate import tags
from overrides import overrides

from scrutiny.htmlutils import show_hide_div, table
from scrutiny.interfaces import ContrastModule, ContrastState
from scrutiny.javacard.modules.jcalgtest import JCAlgTestModule, \
    PerformanceResult


class AlgPerformance(JCAlgTestModule):
    """Scrutiny algorithm performance module"""

    def __init__(self, module_name="Algorithm Performance"):
        super().__init__(module_name)
        self.performance: Dict[str, PerformanceResult] = {}

    @overrides
    def contrast(self, other):
        super().contrast(other)

        matching = {}
        erroneous = {}
        missing = {}
        mismatch = {}
        skipped = {}

        for key in self.performance:

            if key not in other.performance.keys():
                missing[key] = [self.performance[key], None]
                continue

            ref: PerformanceResult = self.performance[key]
            prof: PerformanceResult = other.performance[key]

            if ref.error != prof.error:
                erroneous[key] = [ref, prof]
                continue

            if ref.error:
                matching[key] = [ref, prof]
                continue

            if ref.operation_avg() <= 2 and prof.operation_avg() <= 2:
                skipped[key] = [ref, prof]
                continue

            avg_diff = abs(ref.operation_avg() - prof.operation_avg())
            if avg_diff > ref.operation_max() - ref.operation_min() \
                    and avg_diff > 0.2 * ref.operation_avg():
                if ref.operation_avg() <= 10 and prof.operation_avg() <= 10:
                    skipped[key] = [ref, prof]
                elif "clearKey()" in key:
                    skipped[key] = [ref, prof]
                else:
                    mismatch[key] = [ref, prof]
                continue

            matching[key] = [ref, prof]

        for key in other.performance.keys():
            if key not in self.performance.keys():
                missing[key] = [None, other.performance[key]]

        contrast_module = AlgPerformanceContrast()
        contrast_module.matching = matching
        contrast_module.erroneous = erroneous
        contrast_module.missing = missing
        contrast_module.mismatch = mismatch
        contrast_module.skipped = skipped

        return [contrast_module]

    @overrides
    def add_result(self, key: str, result: PerformanceResult) -> None:
        self.performance[key] = result


class AlgPerformanceContrast(ContrastModule):
    """Scrutiny algorithm performance contrast module"""

    def __init__(self, module_name="Algorithm Performance"):
        super().__init__(module_name)
        self.matching: Dict[str, List[PerformanceResult]] = {}
        self.erroneous: Dict[str, List[PerformanceResult]] = {}
        self.missing: Dict[str, List[Optional[PerformanceResult]]] = {}
        self.mismatch: Dict[str, List[PerformanceResult]] = {}
        self.skipped: Dict[str, List[PerformanceResult]] = {}

    @overrides
    def get_state(self):
        if self.mismatch:
            return ContrastState.SUSPICIOUS
        if self.missing or self.erroneous:
            return ContrastState.WARN
        return ContrastState.MATCH

    @overrides
    def project_html(self, ref_name: str, prof_name: str) -> None:
        self.output_intro()

        if self.mismatch:
            self.output_mismatch(ref_name, prof_name)

        if self.erroneous:
            self.output_erroneous(ref_name, prof_name)

        if self.missing:
            self.output_missing(ref_name, prof_name)

        if self.matching:
            self.output_matching(ref_name, prof_name)

        if self.skipped:
            self.output_skipped(ref_name, prof_name)

    def output_intro(self):
        """Output introductory section"""

        tags.h3("Algorithm Performance comparison results")
        tags.p("This module compares Java Card "
               "algorithm performance between the cards.")
        tags.p("To learn more about testing methodology, visit")
        tags.a(
            "https://www.fi.muni.cz/~xsvenda/jcalgtest/knowledgebase.html",
            href="https://www.fi.muni.cz/~xsvenda/jcalgtest/knowledgebase.html"
        )
        tags.h4("Overview:")
        tags.p(
            "The cards' performance match in " +
            str(len(self.matching)) + " algorithms."
        )
        tags.p(
            "There are " + str(len(self.missing)) +
            " algorithms with missing results for either card."
        )
        tags.p(
            "There are " + str(len(self.mismatch)) +
            " algorithms with different results."
        )
        tags.p(
            "There are " + str(len(self.erroneous)) +
            " algorithms that failed with different error message."
        )
        tags.p(
            str(len(self.skipped)) +
            " algorithms were omitted due to being too fast in general."
        )

    def output_missing(self, ref_name, prof_name):
        """Output missing measurements section"""

        tags.h4("Missing measurements in algorithm performance:",
                style="color:var(--yellow-color);display:inline-block")

        header = ["Algorithm",
                  ref_name + " (reference)",
                  prof_name + " (profiled)"]

        data = []
        for key in self.missing:
            ref = self.missing[key][0]
            prof = self.missing[key][1]

            reftext = "Failed: " + str(ref.error)
            proftext = "Failed: " + str(prof.error)

            if not ref:
                reftext = "Result missing"
            elif not ref.error:
                reftext = "{:.2f}".format(ref.operation_avg()) + " ms"

            if not prof:
                proftext = "Result missing"
            elif not prof.error:
                proftext = "{:.2f}".format(prof.operation_avg()) + " ms"

            data.append([key, reftext, proftext])

        sm_div = show_hide_div("performance_missing_div", hide=True)

        with sm_div:
            tags.p(
                "These are the algorithms which had their results missing on "
                "one of the cards. These should be checked manually."
            )
            table(data, header,
                  green_value="ms",
                  red_value="Failed")

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

            reftext = "Failed: " + str(ref.error)
            proftext = "Failed: " + str(prof.error)

            if not ref.error:
                reftext = "{:.2f}".format(ref.operation_avg()) + " ms"

            if not prof.error:
                proftext = "{:.2f}".format(prof.operation_avg()) + " ms"

            data.append([key, reftext, proftext])

        sm_div = show_hide_div("performance_matching_div", hide=True)

        with sm_div:
            tags.p(
                "These are the algorithms in which the cards performed "
                "similarly, or on which they failed with the same error."
            )
            table(data, header,
                  green_value="ms",
                  red_value="Failed")

    def output_mismatch(self, ref_name, prof_name):
        """Output mismatch section"""

        tags.h4("List of algorithms with different results:",
                style="color:var(--red-color);display:inline-block")

        header = ["Algorithm",
                  ref_name + " (reference)",
                  prof_name + " (profiled)"]

        data = []
        for key in self.mismatch:
            ref = self.mismatch[key][0]
            prof = self.mismatch[key][1]

            reftext = "{:.2f}".format(ref.operation_avg()) + " ms"
            proftext = "{:.2f}".format(prof.operation_avg()) + " ms"

            data.append([key, reftext, proftext])

        sm_div = show_hide_div("performance_mismatch_div", hide=False)

        with sm_div:
            tags.p(
                "These are the algorithms in which the cards performed "
                "with different results."
            )
            table(data, header,
                  red_value="ms")

    def output_erroneous(self, ref_name, prof_name):
        """Output erroneous section"""

        tags.h4("List of algorithms with mismatch in error:",
                style="color:var(--orange-color);display:inline-block")

        header = ["Algorithm",
                  ref_name + " (reference)",
                  prof_name + " (profiled)"]

        data = []
        for key in self.erroneous:
            ref = self.erroneous[key][0]
            prof = self.erroneous[key][1]

            reftext = "Failed: " + str(ref.error)
            proftext = "Failed: " + str(prof.error)

            if not ref.error:
                reftext = "{:.2f}".format(ref.operation_avg()) + " ms"

            if not prof.error:
                proftext = "{:.2f}".format(prof.operation_avg()) + " ms"

            data.append([key, reftext, proftext])

        sm_div = show_hide_div("performance_erroneous_div", hide=False)

        with sm_div:
            tags.p(
                "These are the algorithms in which the cards failed with "
                "different error. You should manually check this table."
                "The errors were probably caused by random exceptions during "
                "performance testing. It is recommended to rerun these "
                "algorithms manually to ascertain that the card is not broken."
            )
            table(data, header,
                  green_value="ms",
                  red_value="Failed")

    def output_skipped(self, ref_name, prof_name):
        """Output skipped section"""

        tags.h4("List of algorithms not used for verification:",
                style="display:inline-block")

        header = ["Algorithm",
                  ref_name + " (reference)",
                  prof_name + " (profiled)"]

        data = []
        for key in self.skipped:
            ref = self.skipped[key][0]
            prof = self.skipped[key][1]

            reftext = "Failed: " + str(ref.error)
            proftext = "Failed: " + str(prof.error)

            if not ref.error:
                reftext = "{:.2f}".format(ref.operation_avg()) + " ms"

            if not prof.error:
                proftext = "{:.2f}".format(prof.operation_avg()) + " ms"

            data.append([key, reftext, proftext])

        sm_div = show_hide_div("performance_skipped_div", hide=True)

        with sm_div:
            tags.p(
                "These are the algorithms that run fast overall. Differences "
                "of few milliseconds can happen due to measurement errors. "
                "These measurements have information value, but are omitted "
                "in automated mismatch detection."
            )
            table(data, header,
                  green_value="ms",
                  red_value="Failed")

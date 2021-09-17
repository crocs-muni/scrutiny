from dominate import tags
from overrides import overrides

from scrutiny.htmlutils import show_hide_div
from typing import Dict
from scrutiny.interfaces import ContrastModule, ContrastState, Module

class TraceComparisonResult:
    def __init__(self) -> None:
        self.is_supported = None
        self.is_visible = None
        self.metric = None
        self.metric_result = None
        self.in_matching_interval = None
        self.in_warn_interval = None
        self.traces_image_path = None

class TracesComparerModule(Module):
    """
    Base class for Traces comparer module
    """

    def __init__(self, module_name):
        self.module_name = module_name

    @overrides
    def contrast(self, other):
        """
        Produce contrast module by comparing self to other module
        In our context this is done by our application in java, compares reference profile with new profile
        Or here can be done verification whether result of the metric that will be in output json is in threshold
        :param other: other module of the same type
        :return: list of contrast modules
        """
        return []

class TracesComparerContrast(ContrastModule):
    """
    Traces comparer contrast module
    """

    def __init__(self, module_name = "Traces Comparer"):
        super().__init__(module_name)
        self.matching : Dict[str, TraceComparisonResult] = {}

    @overrides
    def get_state(self):
        if ("SUSPICIOUS" in self.result):
            return ContrastState.SUSPICIOUS
        elif ("WARN" in self.result):
            return ContrastState.WARN
        return ContrastState.MATCH

    @overrides
    def project_html(self, ref_name, prof_name):        
        self.output_intro()
        operation_count = 0
        for key in self.matching:
            operation_count += 1
            trace_comparison_result : TraceComparisonResult = self.matching[key]        
            operation_divname = key + str(operation_count)

            if (not trace_comparison_result.is_supported):
                self.output_not_supported(key, operation_divname, trace_comparison_result)
            elif (not trace_comparison_result.is_visible):
                self.output_invisible(key, operation_divname, trace_comparison_result)
            elif (trace_comparison_result.in_matching_interval):
                self.output_matching(key, operation_divname, trace_comparison_result)
            elif (trace_comparison_result.in_warn_interval):
                self.output_not_matching(key, operation_divname, trace_comparison_result)
            else:
                self.output_not_matching(key, operation_divname, trace_comparison_result)

    def output_intro(self) -> None:
        tags.h3("Power traces comparison results")
        tags.p("This module compares Java Card power traces.")
        tags.p("To learn more about testing methodology, visit")
        tags.a(
            "https://www.fi.muni.cz/~xsvenda/jcalgtest/knowledgebase.html",
            href="https://www.fi.muni.cz/~xsvenda/jcalgtest/knowledgebase.html"
        )
        tags.br()
        tags.br()

    def output_matching(self, operation : str,  operation_divname : str, trace_comparison_result : TraceComparisonResult) -> None:
        tags.span(cls="dot match")
        tags.h2("Operation: " + operation, style="display: inline-block;")
        operation_div = show_hide_div(operation_divname, hide=True)
        with operation_div:
            tags.p("Metric used: " + str(trace_comparison_result.metric))
            tags.p("Metric result: " + str(trace_comparison_result.metric_result))
            tags.img(src=str(trace_comparison_result.traces_image_path))

    def output_not_matching(self, operation : str,  operation_divname : str, trace_comparison_result : TraceComparisonResult) -> None:
        tags.span(cls="dot suspicious")
        tags.h2("Operation: " + operation, style="display: inline-block;")
        operation_div = show_hide_div(operation_divname, hide=True)
        with operation_div:
            tags.p("Metric used: " + str(trace_comparison_result.metric))
            tags.p("Metric result: " + str(trace_comparison_result.metric_result))
            tags.img(src=str(trace_comparison_result.traces_image_path))

    def output_invisible(self, operation : str,  operation_divname : str, trace_comparison_result : TraceComparisonResult) -> None:
        tags.span(cls="dot warn")
        tags.h2("Operation: " + operation, style="display: inline-block;")
        operation_div = show_hide_div(operation_divname, hide=True)
        with operation_div:
            tags.p("Metric used: " + str(trace_comparison_result.metric))
            tags.p("Metric result: " + str(trace_comparison_result.metric_result))
            tags.img(src=str(trace_comparison_result.traces_image_path))

    def output_not_supported(self, operation : str, operation_divname : str, trace_comparison_result : TraceComparisonResult) -> None:
        tags.span(cls="dot suspicious")
        tags.h2("Operation: " + operation, style="display: inline-block;")
        operation_div = show_hide_div(operation_divname, hide=True)
        with operation_div:
            tags.p("Metric used: " + str(trace_comparison_result.metric))
            tags.p("Metric result: " + str(trace_comparison_result.metric_result))
            tags.img(src=str(trace_comparison_result.traces_image_path))

        
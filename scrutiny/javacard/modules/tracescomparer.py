from distutils.ccompiler import new_compiler
from hashlib import new
from dominate import tags
from overrides import overrides
from scrutiny.device import Device

from scrutiny.htmlutils import show_hide_div
from typing import Dict, List
from scrutiny.interfaces import ContrastModule, ContrastState, Module

from statistics import mean, variance
from math import sqrt
from scipy.stats import norm

class TCOComparison:
    def __init__(self)  -> None:
        self.distance : float = 0
        self.file_path : str = None

class TCOOperationExecTime:
    def __init__(self) -> None:
        self.unit : str = None
        self.time : float = 0

class TCOOperationPipelineComparisons:
    def __init__(self) -> None:
        self.pipeline : str = None
        self.comparisons : List[TCOComparison] = []

class TCOOperation:
    def __init__(self) -> None:
        self.operation_code : str = None
        self.comparisons : List[TCOOperationPipelineComparisons] = []
        self.execution_times : List[TCOOperationExecTime] = []
        self.operation_present : bool = False

class TracesComparerOutput:
    def __init__(self) -> None:
        self.card_code : str = None
        self.created_date : str = None
        self.created_by : str = None
        self.additional_info : str = None
        self.results : List[TCOOperation] = []

# SCRUTINY contrast related

class OperationComparisonResult:
    def __init__(self) -> None:
        self.distance_value : str = None
        self.image_path : str = None
        self.comparison_state : str = None

class PipelineResult:
    def __init__(self) -> None:
        self.pipeline_code : str = None
        self.match_upper_bound : float = 0
        self.warn_upper_bound : float = 0
        self.comparison_state : str = None
        self.comparison_results : List[OperationComparisonResult] = []

class OperationResult:
    def __init__(self) -> None:
        self.operation_code : str = None
        self.operation_present : bool = None
        self.comparison_results : List[PipelineResult] = []
        self.ref_execution_times : List[TCOOperationExecTime] = []
        self.new_execution_times : List[TCOOperationExecTime] = []
        self.comparison_state : str = None

# Device, module and contrast

class TraceComparerDevice(Device):
    def __init___(self, name, device_type) -> None:
        super(name, device_type)
        self.modules : Dict[str, TracesComparerModule] = {}

class TracesComparerModule(Module):
    """
    Base class for Traces comparer module
    """

    def __init__(self, module_name):
        self.module_name : str = module_name
        self.module_data : Dict[str, TracesComparerOutput] = {}

    def getStateMeasurement(self, measurementValue : float, matchUpperBound : float, warnUpperBound : float) -> ContrastState:
        if (measurementValue < matchUpperBound):
            return ContrastState.MATCH
        elif (measurementValue < warnUpperBound):
            return ContrastState.WARN
        else:
            return ContrastState.SUSPICIOUS

    def getStateComparisonResults(self, comparisonResults : List[OperationComparisonResult]) -> ContrastState:
        for i in range(len(comparisonResults)):
            if (str(comparisonResults[i].comparison_state) == str(ContrastState.SUSPICIOUS)):
                return ContrastState.SUSPICIOUS
            if (str(comparisonResults[i].comparison_state) == str(ContrastState.WARN)):
                return ContrastState.WARN
        return ContrastState.MATCH

    def getStateOperationResults(self, comparisonResults : List[OperationResult]) -> ContrastState:
        for i in range(len(comparisonResults)):
            if (comparisonResults[i].comparison_state == str(ContrastState.SUSPICIOUS)):
                return ContrastState.SUSPICIOUS
            if (comparisonResults[i].comparison_state == str(ContrastState.WARN)):
                return ContrastState.WARN
        return ContrastState.MATCH

    def getStatePipelineResults(self, pipelineResults : List[PipelineResult]) -> ContrastState:
        for i in range(len(pipelineResults)):
            if (str(pipelineResults[i].comparison_state) == str(ContrastState.SUSPICIOUS)):
                return ContrastState.SUSPICIOUS
            if (str(pipelineResults[i].comparison_state) == str(ContrastState.WARN)):
                return ContrastState.WARN
        return ContrastState.MATCH
        
    @overrides
    def contrast(self, other):
        ref : TracesComparerOutput = self.module_data
        prof : TracesComparerOutput = other.module_data
        operationResults : List[OperationResult] = []
        for newOperation in prof.results:
            refOperation = next((o for o in ref.results if o.operation_code == newOperation.operation_code), None)
            if (refOperation == None):
                continue

            if (not newOperation.operation_present):
                operationResult : OperationResult = OperationResult()
                operationResult.operation_present = False
                operationResult.operation_code = refOperation.operation_code
                operationResult.comparison_state = ContrastState.SUSPICIOUS
                operationResults.append(operationResult)
                continue

            pipelineResults : List[PipelineResult] = []
            for refPipeline in refOperation.comparisons:
                ref_measurement_distances = [comparison.distance for comparison in refPipeline.comparisons]
                n : int = len(ref_measurement_distances)
                m : float = mean(ref_measurement_distances)
                sigma = sqrt(variance(ref_measurement_distances))
                qnorm95 : float = norm.ppf(0.95)
                qnorm99 : float = norm.ppf(0.99)
                matchUpperBound : float = float(m+((sigma/sqrt(n))*qnorm95))
                warnUpperBound : float = float(m+((sigma/sqrt(n))*qnorm99))

                newPipeline = next((p for p in newOperation.comparisons if p.pipeline == refPipeline.pipeline), None)
                if (newPipeline == None):
                    continue
                operationComparisonResults : List[OperationComparisonResult] = []
                for newPipelineComparison in newPipeline.comparisons:
                    ocr = OperationComparisonResult()
                    ocr.distance_value = newPipelineComparison.distance
                    ocr.image_path = newPipelineComparison.file_path
                    ocr.comparison_state = str(self.getStateMeasurement(ocr.distance_value, matchUpperBound, warnUpperBound))
                    operationComparisonResults.append(ocr)

                piRes : PipelineResult = PipelineResult()
                piRes.pipeline_code = refPipeline.pipeline
                piRes.match_upper_bound = matchUpperBound
                piRes.warn_upper_bound = warnUpperBound
                piRes.comparison_state = str(self.getStateComparisonResults(operationComparisonResults))
                piRes.comparison_results = operationComparisonResults
                pipelineResults.append(piRes)

            operationResult : OperationResult = OperationResult()
            operationResult.operation_code = refOperation.operation_code
            operationResult.comparison_results = pipelineResults
            operationResult.comparison_state = str(self.getStatePipelineResults(pipelineResults))
            operationResult.ref_execution_times = refOperation.execution_times
            operationResult.new_execution_times = newOperation.execution_times
            operationResult.operation_present = True
            operationResults.append(operationResult)

        contrast : TracesComparerContrast = TracesComparerContrast()
        contrast.results = operationResults
        contrast.result = str(self.getStateOperationResults(operationResults))
        
        return [contrast]

class TracesComparerContrast(ContrastModule):
    """
    Traces comparer contrast module
    """

    def __init__(self, module_name = "Traces Comparer"):
        super().__init__(module_name)
        self.results : List[OperationResult] = []

    @overrides
    def get_state(self):
        if (str(ContrastState.SUSPICIOUS) == str(self.result)):
            return ContrastState.SUSPICIOUS
        elif (str(ContrastState.WARN) == str(self.result)):
            return ContrastState.WARN
        return ContrastState.MATCH

    @overrides
    def project_html(self, ref_name, prof_name):        
        self.output_intro()
        for operationResult in self.results:
            operation_divname = operationResult.operation_code
            if (not operationResult.operation_present):
                self.output_not_supported(operation_divname, operationResult)
                continue
            if (operationResult.comparison_state == str(ContrastState.MATCH)):
                tags.span(cls="dot match")
            elif (operationResult.comparison_state == str(ContrastState.WARN)):
                tags.span(cls="dot warn")
            else:
                tags.span(cls="dot suspicious")
            tags.h2("Operation: " + operationResult.operation_code, style="display: inline-block;")
            operation_div = show_hide_div(operation_divname, hide=True)
            with operation_div:
                for pipelineResult in operationResult.comparison_results:
                    pipeline_divname = operation_divname + "-" + pipelineResult.pipeline_code
                    if (pipelineResult.comparison_state == str(ContrastState.MATCH)):
                        tags.span(cls="dot match")
                    elif (pipelineResult.comparison_state == str(ContrastState.WARN)):
                        tags.span(cls="dot warn")
                    else:
                        tags.span(cls="dot suspicious")
                    tags.h2("Pipeline: " + pipelineResult.pipeline_code, style="display: inline-block;")
                    pipeline_div = show_hide_div(pipeline_divname, hide=True)
                    with pipeline_div:
                        comparison_count = 0
                        for comparisonResult in pipelineResult.comparison_results:
                            comparison_count += 1
                            comparison_divname = pipeline_divname + "-" + str(comparison_count)
                            self.output_comparison(comparison_count, comparison_divname, operationResult, pipelineResult, comparisonResult)

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

    def output_comparison(self, comparisonCount : int, divname : str, operationResult : OperationResult, pipelineResult : PipelineResult, operationComparisonResult : OperationComparisonResult) -> None:
        if (operationComparisonResult.comparison_state == str(ContrastState.MATCH)):
            tags.span(cls="dot match")
        elif (operationComparisonResult.comparison_state == str(ContrastState.WARN)):
            tags.span(cls="dot warn")
        else:
            tags.span(cls="dot suspicious")

        tags.h2("Comparison " + str(comparisonCount), style="display: inline-block;")
        comparison_div = show_hide_div(divname, hide=True)
        with comparison_div:
            tags.p("Metric result: " + str(operationComparisonResult.distance_value))
            tags.img(src=operationComparisonResult.image_path)

    def output_not_supported(self, operation_divname : str, operationResult : OperationResult) -> None:
        tags.span(cls="dot suspicious")
        tags.h2("Operation: " + operationResult, style="display: inline-block;")
        operation_div = show_hide_div(operation_divname, hide=True)
        with operation_div:
            tags.p("This operation was not present in the new measured profile, however in the reference it was.")
        
from dominate import tags
from overrides import overrides
from scrutiny.device import Device

from scrutiny.htmlutils import generate_gallery, show_hide_div_right, generate_piechart
from typing import Dict, List, Tuple
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
        self.metric_type : str = None

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
        self.match_bound : float = 0
        self.warn_bound : float = 0
        self.metric_type : str = None
        self.comparison_state : str = None
        self.comparison_results : List[OperationComparisonResult] = []

class OperationResult:
    def __init__(self) -> None:
        self.operation_code : str = None
        self.operation_present : bool = None
        self.comparison_results : List[PipelineResult] = []
        self.exec_time_match_lower_bound : float = 0
        self.exec_time_match_upper_bound : float = 0
        self.exec_time_warn_lower_bound : float = 0
        self.exec_time_warn_upper_bound : float = 0
        self.exec_times : List[TCOOperationExecTime] = []
        self.exec_time_state : ContrastState = None
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

    def getStateMeasurement(self, measurementValue : float, matchBound : float, warnBound : float, metric_type : str) -> ContrastState:
        if (metric_type == "distance"):
            if (measurementValue < matchBound):
                return ContrastState.MATCH
            elif (measurementValue < warnBound):
                return ContrastState.WARN
            else:
                return ContrastState.SUSPICIOUS
        else:
            if (measurementValue > matchBound):
                return ContrastState.MATCH
            elif (measurementValue > warnBound):
                return ContrastState.WARN
            else:
                return ContrastState.SUSPICIOUS

    def getStateComparisonResults(self, comparisonResults : List[OperationComparisonResult]) -> ContrastState:
        for i in range(len(comparisonResults)):
            if (comparisonResults[i].comparison_state == str(ContrastState.SUSPICIOUS)):
                return ContrastState.SUSPICIOUS
            if (comparisonResults[i].comparison_state == str(ContrastState.WARN)):
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
            if (pipelineResults[i].comparison_state == str(ContrastState.SUSPICIOUS)):
                return ContrastState.SUSPICIOUS
            if (pipelineResults[i].comparison_state == str(ContrastState.WARN)):
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
                matchBound = self.getMetricMatchBound(refPipeline)
                warnBound = self.getMetricWarnBound(refPipeline)

                newPipeline = next((p for p in newOperation.comparisons if p.pipeline == refPipeline.pipeline), None)
                if (newPipeline == None):
                    continue
                operationComparisonResults : List[OperationComparisonResult] = []
                for newPipelineComparison in newPipeline.comparisons:
                    ocr = OperationComparisonResult()
                    ocr.distance_value = newPipelineComparison.distance
                    ocr.image_path = newPipelineComparison.file_path
                    ocr.comparison_state = str(self.getStateMeasurement(ocr.distance_value, matchBound, warnBound, refPipeline.metric_type))
                    operationComparisonResults.append(ocr)

                piRes : PipelineResult = PipelineResult()
                piRes.pipeline_code = refPipeline.pipeline
                piRes.match_bound = matchBound
                piRes.warn_bound = warnBound
                piRes.metric_type = refPipeline.metric_type
                piRes.comparison_state = str(self.getStateComparisonResults(operationComparisonResults))
                piRes.comparison_results = operationComparisonResults
                pipelineResults.append(piRes)

            exec_time_match_bounds = self.getExecTimeMatchBound(refOperation)
            exec_time_warn_bounds = self.getExecTimeWarnBound(refOperation)
            operationResult : OperationResult = OperationResult()
            operationResult.operation_code = refOperation.operation_code
            operationResult.comparison_results = pipelineResults
            operationResult.comparison_state = str(self.getStatePipelineResults(pipelineResults))
            operationResult.exec_time_match_lower_bound = exec_time_match_bounds[0]
            operationResult.exec_time_match_upper_bound = exec_time_match_bounds[1]
            operationResult.exec_time_warn_lower_bound = exec_time_warn_bounds[0]
            operationResult.exec_time_warn_upper_bound = exec_time_warn_bounds[1]
            operationResult.exec_times = newOperation.execution_times
            operationResult.new_execution_times = newOperation.execution_times
            operationResult.operation_present = True
            operationResults.append(operationResult)

        contrast : TracesComparerContrast = TracesComparerContrast()
        contrast.results = operationResults
        contrast.result = str(self.getStateOperationResults(operationResults))
        
        return [contrast]

    def getMetricWarnBound(self, refPipeline : TCOOperationPipelineComparisons): 
        ref_measurement_distances = [comparison.distance for comparison in refPipeline.comparisons]
        n : int = len(ref_measurement_distances)
        m : float = mean(ref_measurement_distances)
        sigma = sqrt(variance(ref_measurement_distances))   
        qnorm99 : float = norm.ppf(0.99)
        warnBound : float = float(m+((sigma/sqrt(n))*qnorm99)) if refPipeline.metric_type == "distance" else float(m-((sigma/sqrt(n))*qnorm99))
        return warnBound

    def getMetricMatchBound(self, refPipeline : TCOOperationPipelineComparisons):
        ref_measurement_distances = [comparison.distance for comparison in refPipeline.comparisons]
        n : int = len(ref_measurement_distances)
        m : float = mean(ref_measurement_distances)
        sigma = sqrt(variance(ref_measurement_distances))
        qnorm95 : float = norm.ppf(0.95)
        matchBound : float = float(m+((sigma/sqrt(n))*qnorm95)) if refPipeline.metric_type == "distance" else float(m-((sigma/sqrt(n))*qnorm95))
        return matchBound

    def getExecTimeWarnBound(self, refOperation : TCOOperation) -> Tuple[float, float]:
        ref_exec_times = [et.time for et in refOperation.execution_times]
        n : int = len(ref_exec_times)
        m : float = mean(ref_exec_times)
        sigma = sqrt(variance(ref_exec_times))
        qnorm99 : float = norm.ppf(1-(0.01/2))
        return (float(m-((sigma/sqrt(n))*qnorm99)), float(m+((sigma/sqrt(n))*qnorm99)))

    def getExecTimeMatchBound(self, refOperation : TCOOperation) -> Tuple[float, float]:
        ref_exec_times = [et.time for et in refOperation.execution_times]
        n : int = len(ref_exec_times)
        m : float = mean(ref_exec_times)
        sigma = sqrt(variance(ref_exec_times))
        qnorm95 : float = norm.ppf(1-(0.05/2))
        return (float(m-((sigma/sqrt(n))*qnorm95)), float(m+((sigma/sqrt(n))*qnorm95)))

class TracesComparerContrast(ContrastModule):
    """
    Traces comparer contrast module
    """

    COLORS : List[Tuple[int, int, int]] = [(76,175,80), (211,208,62), (192,68,68)]

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
            matches = 0
            warns = 0
            suspicious = 0
            for pipelineResult in operationResult.comparison_results:
                matches += len([cr for cr in pipelineResult.comparison_results if cr.comparison_state == str(ContrastState.MATCH)])
                warns += len([cr for cr in pipelineResult.comparison_results if cr.comparison_state == str(ContrastState.WARN)])
                suspicious += len([cr for cr in pipelineResult.comparison_results if cr.comparison_state == str(ContrastState.SUSPICIOUS)])
            comparisons_count = matches + warns + suspicious
            comparison_percentages = [matches*100/(comparisons_count), warns*100/comparisons_count, suspicious*100/comparisons_count]
            pie_chart_style = generate_piechart(comparison_percentages, TracesComparerContrast.COLORS)
            tags.figure("", style = pie_chart_style)
            tags.h2("Operation: " + operationResult.operation_code, style="display: inline-block;")
            operation_div = show_hide_div_right(operation_divname, hide=True)
            with operation_div:
                for pipelineResult in operationResult.comparison_results:
                    matches = len([cr for cr in pipelineResult.comparison_results if cr.comparison_state == str(ContrastState.MATCH)])
                    warns = len([cr for cr in pipelineResult.comparison_results if cr.comparison_state == str(ContrastState.WARN)])
                    suspicious = len([cr for cr in pipelineResult.comparison_results if cr.comparison_state == str(ContrastState.SUSPICIOUS)])
                    comparisons_count = len(pipelineResult.comparison_results)
                    comparison_percentages = [matches*100/comparisons_count, warns*100/comparisons_count, suspicious*100/comparisons_count]
                    pie_chart_style = generate_piechart(comparison_percentages, TracesComparerContrast.COLORS)
                    tags.figure("", style = pie_chart_style)
                    tags.h2("Pipeline: " + pipelineResult.pipeline_code, style="display: inline-block;")
                    image_paths = [ip.image_path for ip in pipelineResult.comparison_results]
                    generate_gallery(image_paths)
                    with tags.table():
                        with tags.tr():
                            tags.th("Comparison")
                            tags.th("Metric type")
                            tags.th("Match bound")
                            tags.th("Warn bound")
                            tags.th("Comparison value")
                            tags.th("State")
                        for comparison_result in pipelineResult.comparison_results:
                            with tags.tr():
                                tags.td(comparison_result.image_path)
                                tags.td(pipelineResult.metric_type)
                                tags.td(round(pipelineResult.match_bound, 4))
                                tags.td(round(pipelineResult.warn_bound, 4))
                                tags.td(round(comparison_result.distance_value, 4))
                                tags.td(self.getState(comparison_result.comparison_state), style=self.getStateStyle(comparison_result.comparison_state))
                
                tags.br()
                tags.h3("Execution times section")
                with tags.table():
                    with tags.tr():
                        tags.th("Measurement")
                        tags.th("Match bounds")
                        tags.th("Warn bounds")
                        tags.th("Execution time value")
                        tags.th("State")
                    et_count = 1
                    for et in operationResult.exec_times:
                        etmlb = operationResult.exec_time_match_lower_bound
                        etmub = operationResult.exec_time_match_upper_bound
                        etwlb = operationResult.exec_time_warn_lower_bound
                        etwub = operationResult.exec_time_warn_upper_bound
                        state = str(self.getStateExecTime(etmlb, etmub, etwlb, etwub, et.time))
                        with tags.tr():
                            tags.td("Execution time " + str(et_count))
                            tags.td("({lb}, {ub})".format(
                                lb = round(etmlb, 4),
                                ub = round(etmub, 4)))
                            tags.td("({lb}, {ub})".format(
                                lb = round(etwlb, 4),
                                ub = round(etwub, 4)))
                            tags.td(round(et.time, 4))
                            tags.td(self.getState(state), style = self.getStateStyle(state))
                        et_count += 1


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

    def output_not_supported(self, operation_divname : str, operationResult : OperationResult) -> None:
        tags.span(cls="dot suspicious")
        tags.h2("Operation: " + operationResult, style="display: inline-block;")
        operation_div = show_hide_div_right(operation_divname, hide=True)
        with operation_div:
            tags.p("This operation was not present in the new measured profile, however in the reference it was.")

    def getState(self, state : str) -> str:
        if (state == str(ContrastState.MATCH)):
            return "MATCH"
        elif (state == str(ContrastState.WARN)):
            return "WARN"
        else:
            return "SUSPICIOUS"

    def getStateStyle(self, state : str) -> str:
        if (state == str(ContrastState.MATCH)):
            return "color: var(--green-color)"
        elif (state == str(ContrastState.WARN)):
            return "color: var(--yellow-color)"
        else:
            return "color: var(--red-color)"

    def getStateExecTime(
        self,
        match_lower_bound : float,
        match_upper_bound : float,
        warn_lower_bound : float,
        warn_upper_bound : float,
        time : float):
        if (time > match_lower_bound and time < match_upper_bound):
            return ContrastState.MATCH
        elif (time > warn_lower_bound and time < warn_upper_bound):
            return ContrastState.WARN
        else:
            return ContrastState.SUSPICIOUS

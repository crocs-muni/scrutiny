import re
from dominate import tags
from overrides import overrides

from scrutiny.htmlutils import show_hide_div_right
from typing import List
from scrutiny.interfaces import ContrastModule, ContrastState


class CardDBCResult:
    def __init__(self) -> None:
        self.card_code : str = None
        self.operation_results : List[OperationDBCResult] = []

    def is_card_unclassified(self) -> bool:
        is_unclassified : bool = True
        for operations_result in self.operations_results:
            if (len(operations_result.similarity_intervals) > 0):
                is_unclassified = False
        return is_unclassified

    def get_found_count(self):
        found_count : int = 0
        for operations_result in self.operations_results:
            if (len(operations_result.similarity_intervals) > 0):
                found_count += 1
        return found_count

class OperationDBCResult:
    def __init__(self) -> None:
        self.operation_code : str = None
        self.similarity_intervals : List[SimilarityInterval] = []
        self.visualized_operations : str = None

class SimilarityInterval:
    def __init__(self) -> None:
        self.similarity_value : float = 0
        self.similarity_value_type : str = None
        self.time_from : float = 0
        self.time_to : float = 0
        self.indexes_compared : int = 0


class TraceClassifierContrast(ContrastModule):
    """
    Traces comparer contrast module
    """

    def __init__(self, module_name = "Trace Classifier"):
        super().__init__(module_name)
        self.results : List[CardDBCResult] = []
        
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
        for result in self.results:
            card_divname = result.card_code
            tags.figure(result.get_found_count(), cls="circle")
            tags.h2("Operation: " + result.card_code, style="display: inline-block;")
            card_div = show_hide_div_right(card_divname, hide=True)
            with card_div:
                if (result.is_card_unclassified()):
                    tags.h3("Trace contains no known operations from this card", style="display: inline-block;")
                    continue
                
                for op_res in result.operations_results:
                    operation_divname = card_divname + op_res.operation_code
                    tags.figure(len(op_res.similarity_intervals), cls="circle")
                    tags.h2("Operation " + op_res.operation_code, style="display: inline-block;")
                    operation_div = show_hide_div_right(operation_divname, hide=True)
                    with operation_div:
                        if (len(op_res.similarity_intervals) == 0):
                            tags.h3("Trace contains no operations", style="display: inline-block;")
                            continue

                        image_id = op_res.operation_code
                        tags.img(
                            id = image_id,
                            src = op_res.visualized_operations,
                            alt = op_res.visualized_operations,
                            style = "display: inline-block; width: 100%")

                        operation_divname_details = card_divname + op_res.operation_code + "-details"
                        tags.h2("Classification details", style="display: inline-block;")
                        details_div = show_hide_div_right(operation_divname_details+"-details", hide=True)
                        with details_div:
                            with tags.table():
                                with tags.tr():
                                    tags.th("Time from")
                                    tags.th("Time to")
                                    tags.th("Comparison type")
                                    tags.th("Comparison value")
                                for interval in op_res.similarity_intervals:
                                    with tags.tr():
                                        tags.td(round(interval.time_from, 4))
                                        tags.td(round(interval.time_to, 4))
                                        tags.td(interval.similarity_value_type)
                                        tags.td(round(interval.similarity_value, 4))
                            tags.br()


    def output_intro(self) -> None:
        tags.h3("Power trace classification results")
        tags.p("This module classifies Java Card power traces.")
        tags.p("To learn more about testing methodology, visit")
        tags.a(
            "https://www.fi.muni.cz/~xsvenda/jcalgtest/knowledgebase.html",
            href="https://www.fi.muni.cz/~xsvenda/jcalgtest/knowledgebase.html"
        )
        tags.br()
        tags.br()

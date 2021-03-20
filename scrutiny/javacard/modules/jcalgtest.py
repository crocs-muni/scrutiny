from typing import Optional, List

from scrutiny.interfaces import Module


class JCAlgTestModule(Module):
    """
    Common base for JCAlgTest modules
    """

    def __init__(self, module_name):
        super().__init__(module_name)
        self.test_info = {}
        self.jcsystem = {}
        self.apdu = {}
        self.cplc = {}

    def add_result(self, key: str, result: object) -> None:
        """Abstract method to add any result"""


class PerformanceResult:
    """
    Class to store results of algorithm performance testing
    """

    def __init__(self) -> None:
        self.prepare_ins: Optional[int] = None
        self.measure_ins: Optional[int] = None
        self.config: Optional[str] = None

        self.baseline: List[float] = []
        self.operation: List[float] = []

        self.data_length: Optional[int] = None
        self.iterations: Optional[int] = None
        self.invocations: Optional[int] = None

        self.error: Optional[str] = None

    def baseline_avg(self) -> float:
        """Average baseline measurement"""
        return sum(self.baseline) / len(self.baseline)

    def baseline_min(self) -> float:
        """Minimal baseline measurement"""
        return min(self.baseline)

    def baseline_max(self) -> float:
        """Maximal baseline measurement"""
        return max(self.baseline)

    def ipm(self) -> int:
        """
        Algorithm iterations per measurement
        :return: iterations / len(operation)
        """
        if self.iterations % len(self.operation) != 0:
            raise Exception(
                "Total iterations count is not multiple of operation data length"
            )
        return int(self.iterations / len(self.operation))

    def operation_avg(self) -> float:
        """Average single algorithm execution time"""
        return sum(self.operation) / len(self.operation) / self.ipm()

    def operation_min(self) -> float:
        """Minimal single algorithm execution time"""
        return min(self.operation) / self.ipm()

    def operation_max(self) -> float:
        """Maximal single algorithm execution time"""
        return max(self.operation) / self.ipm()

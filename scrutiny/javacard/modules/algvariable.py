from typing import Dict, List

from scrutiny.interfaces import ContrastModule
from scrutiny.javacard.modules.jcalgtest import JCAlgTestModule, PerformanceResult


class AlgVariable(JCAlgTestModule):
    """Scrutiny algorithm variable performance module"""

    def __init__(self, module_name="Algorithm Data-Length-Dependent Performance"):
        super().__init__(module_name)
        self.performance: Dict[str, List[PerformanceResult]] = {}

    def contrast(self, other):
        return []

    def add_result(self, key: str, result: PerformanceResult) -> None:
        if key not in self.performance.keys():
            self.performance[key] = []
        self.performance[key].append(result)


class AlgVariableContrast(ContrastModule):
    """Scrutiny algorithm variable performance contrast module"""

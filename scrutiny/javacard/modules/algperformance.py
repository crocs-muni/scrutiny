from typing import Dict

from scrutiny.interfaces import ContrastModule
from scrutiny.javacard.modules.jcalgtest import JCAlgTestModule, PerformanceResult


class AlgPerformance(JCAlgTestModule):
    """Scrutiny algorithm performance module"""

    def __init__(self, module_name="Algorithm Performance"):
        super().__init__(module_name)
        self.performance: Dict[str, PerformanceResult] = {}

    def contrast(self, other):
        return []

    def add_result(self, key: str, result: PerformanceResult) -> None:
        self.performance[key] = result


class AlgPerformanceContrast(ContrastModule):
    """Scrutiny algorithm performance contrast module"""

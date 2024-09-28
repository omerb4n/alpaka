from typing import Optional

from androguard.core.analysis.analysis import ClassAnalysis

from alpaka.class_signature.class_signature_calculator import ClassSignatureCalculator
from alpaka.class_signature.signature import ClassSignature
from alpaka.utils import get_domain_name


class ClassInfo:
    analysis: ClassAnalysis
    is_obfuscated_name: bool
    _signature: Optional[ClassSignature]
    _signature_calculator: ClassSignatureCalculator

    def __init__(self, class_analysis: ClassAnalysis, is_name_obfuscated: bool, signature_calculator: ClassSignatureCalculator):
        self.analysis = class_analysis
        self.is_obfuscated_name = is_name_obfuscated
        self._signature = None
        self._signature_calculator = signature_calculator

    @staticmethod
    def get_class_name(class_name_prefix) -> str:
        """
        get the class name (without prefix) of the given class_name_prefix.
        e.g. "Lcom/example/myapplication/R$attr;" -> "R$attr"
        """
        class_name = get_domain_name(class_name_prefix)
        if class_name[-1] == ';':
            class_name = class_name[:-1]
        return class_name

    @property
    def signature(self):
        if not self._signature:
            self._signature = self._signature_calculator.calculate_class_signature(self.analysis)
        return self._signature

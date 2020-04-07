from dataclasses import dataclass

from androguard.core.analysis.analysis import ClassAnalysis

from alpaka.class_signature.class_signature_calculator import ClassSignatureCalculator
from alpaka.class_signature.signature import ClassSignature
from alpaka.obfuscation_detection.base import DummyObfuscationDetector
from alpaka.utils import get_domain_name


@dataclass
class ClassInfo:
    analysis: ClassAnalysis
    is_obfuscated_name: bool
    _signature: ClassSignature = None

    # TODO: The ClassSignatureCalculator should be configurable! this should be out of the class
    CLASS_SIGNATURE_CALCULATOR = ClassSignatureCalculator(DummyObfuscationDetector(False))

    @staticmethod
    def get_class_name(class_name_prefix):
        class_name = get_domain_name(class_name_prefix)
        if class_name[-1] == ';':
            class_name = class_name[:-1]
        return class_name

    @property
    def signature(self):
        if not self._signature:
            self._signature = ClassInfo.CLASS_SIGNATURE_CALCULATOR.calculate_class_signature(
                self.analysis)
        return self._signature

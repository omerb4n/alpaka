import re
from typing import Generator, List

from androguard.core.analysis.analysis import ClassAnalysis
from androguard.core.bytecodes.dvm import Instruction

from alpaka.class_signature.signature import ClassSignature
from alpaka.class_signature.simhash_utils import calculate_simhash
from alpaka.obfuscation.types import ObfuscationDetector


class ClassSignatureCalculator:

    TYPE_DESCRIPTOR_REGEX = re.compile(
        r'\[*'  # '[' char(s) before type indicate array
        r'(?:'
        r'[VZBSCIJFD]'  # void and primitives
        r'|'
        r'L[^;]*;'  # class descriptors: L<full_class_name>;
        r')'
    )

    def __init__(self, obfuscation_detector: ObfuscationDetector):
        self._obfuscation_detector = obfuscation_detector

    def calculate_class_signature(self, class_analysis: ClassAnalysis) -> ClassSignature:
        return ClassSignature(
            member_count=self._get_member_count(class_analysis),
            method_count=self._get_method_count(class_analysis),
            instructions_count=self._get_instructions_count(class_analysis),
            members_simhash=self._calc_members_simhash(class_analysis),
            methods_params_simhash=self._calc_methods_params_simhash(class_analysis),
            method_returns_simhash=self._calc_methods_returns_simhash(class_analysis),
            instructions_simhash=self._calc_instructions_simhash(class_analysis),
        )

    @classmethod
    def _get_member_count(cls, class_analysis: ClassAnalysis) -> int:
        return len(class_analysis.get_fields())

    @classmethod
    def _get_method_count(cls, class_analysis: ClassAnalysis) -> int:
        return class_analysis.get_nb_methods()

    @classmethod
    def _get_instructions_count(cls, class_analysis: ClassAnalysis):
        return sum((1 for _instruction in cls.iterate_class_instruction(class_analysis)))

    def _calc_members_simhash(self, class_analysis: ClassAnalysis) -> int:
        return calculate_simhash((
            type_descriptor for member in class_analysis.get_fields()
            if not self._obfuscation_detector.is_obfuscated(
                type_descriptor := member.field.get_descriptor()
            )
        ))

    def _calc_methods_params_simhash(self, class_analysis: ClassAnalysis) -> int:
        return calculate_simhash((
            param_type
            for method in class_analysis.get_methods()
            for param_type in self._get_param_types_from_method_descriptor(method.descriptor)
            if not self._obfuscation_detector.is_obfuscated(param_type)
        ))

    @classmethod
    def _get_param_types_from_method_descriptor(cls, method_descriptor: str) -> List[str]:
        concatenated_params = method_descriptor[1:].split(')')[0]
        return cls.TYPE_DESCRIPTOR_REGEX.findall(concatenated_params)

    def _calc_methods_returns_simhash(self, class_analysis: ClassAnalysis) -> int:
        return calculate_simhash((
            return_type for method in class_analysis.get_methods()
            if not self._obfuscation_detector.is_obfuscated(
                return_type := self._get_return_type_from_method_descriptor(method.descriptor)
            )
        ))

    @classmethod
    def _get_return_type_from_method_descriptor(cls, method_descriptor: str) -> str:
        return method_descriptor.split(')')[-1]

    @classmethod
    def _calc_instructions_simhash(cls, class_analysis: ClassAnalysis):
        return calculate_simhash(
            (instruction.get_name() for instruction in cls.iterate_class_instruction(class_analysis)))

    @staticmethod
    def iterate_class_instruction(class_analysis: ClassAnalysis) -> Generator[Instruction, None, None]:
        for method in class_analysis.get_vm_class().get_methods():
            for instruction in method.get_instructions():
                yield instruction

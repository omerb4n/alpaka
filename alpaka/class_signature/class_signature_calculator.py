import re
from typing import Generator, List

from androguard.core.analysis.analysis import ClassAnalysis
from androguard.core.bytecodes.dvm import Instruction

from alpaka.class_signature.signature import ClassSignature
from alpaka.class_signature.simhash_utils import calculate_simhash, calculate_shingle_simhash
from alpaka.class_signature.string_extractor import StringLiteralsExtractor
from alpaka.obfuscation_detection.base import ObfuscationDetector


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
            methods_returns_simhash=self._calc_methods_returns_simhash(class_analysis),
            instructions_simhash=self._calc_instructions_simhash(class_analysis),
            instruction_shingles_simhash=self._calc_instruction_shingles_simhash(class_analysis),
            implemented_interfaces_count=self._get_implemented_interfaces_count(class_analysis),
            implemented_interfaces_simhash=self._calc_implemented_interfaces_simhash(class_analysis),
            superclass_hash=self._calc_superclass_hash(class_analysis),
            string_literals_count=self._get_string_literals_count(class_analysis),
            string_literals_simhash=self._get_string_literals_simhash(class_analysis),
        )

    @classmethod
    def _get_member_count(cls, class_analysis: ClassAnalysis) -> int:
        try:
            return (
                class_analysis.orig_class.class_data_item.get_instance_fields_size()
                + class_analysis.orig_class.class_data_item.get_static_fields_size()
            )
        except AttributeError:
            # For some reason, some of the classes don't have class_data_item, or have None in it.
            # It seems that for all of those classes there are no fields
            # todo: validate this assumption!
            return 0

    @classmethod
    def _get_method_count(cls, class_analysis: ClassAnalysis) -> int:
        return class_analysis.get_nb_methods()

    @classmethod
    def _get_instructions_count(cls, class_analysis: ClassAnalysis):
        return sum((1 for _instruction in cls.iterate_class_instruction(class_analysis)))

    def _calc_members_simhash(self, class_analysis: ClassAnalysis) -> int:
        try:
            members = class_analysis.orig_class.class_data_item.get_fields()
        except AttributeError:
            members = []
        return calculate_simhash((
            type_descriptor for member in members
            if not self._obfuscation_detector.is_class_name_obfuscated(
                type_descriptor := member.class_name
            )
        ))

    def _calc_methods_params_simhash(self, class_analysis: ClassAnalysis) -> int:
        return calculate_simhash((
            param_type
            for method in class_analysis.get_methods()
            for param_type in self._get_param_types_from_method_descriptor(method.descriptor)
            if not self._obfuscation_detector.is_class_name_obfuscated(param_type)
        ))

    @classmethod
    def _get_param_types_from_method_descriptor(cls, method_descriptor: str) -> List[str]:
        concatenated_params = method_descriptor[1:].split(')')[0]
        return cls.TYPE_DESCRIPTOR_REGEX.findall(concatenated_params)

    def _calc_methods_returns_simhash(self, class_analysis: ClassAnalysis) -> int:
        return calculate_simhash((
            return_type for method in class_analysis.get_methods()
            if not self._obfuscation_detector.is_class_name_obfuscated(
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

    @classmethod
    def _calc_instruction_shingles_simhash(cls, class_analysis: ClassAnalysis):
        return calculate_shingle_simhash(
            (instruction.get_name() for instruction in cls.iterate_class_instruction(class_analysis)))

    @staticmethod
    def iterate_class_instruction(class_analysis: ClassAnalysis) -> Generator[Instruction, None, None]:
        for method in class_analysis.get_vm_class().get_methods():
            for instruction in method.get_instructions():
                yield instruction

    @classmethod
    def _get_implemented_interfaces_count(cls, class_analysis) -> int:
        return len(class_analysis.implements)

    def _calc_implemented_interfaces_simhash(self, class_analysis) -> int:
        return calculate_simhash((
            interface_descriptor
            for interface_descriptor in class_analysis.implements
            if not self._obfuscation_detector.is_class_name_obfuscated(interface_descriptor)
        ))

    def _calc_superclass_hash(self, class_analysis) -> int:
        if self._obfuscation_detector.is_class_name_obfuscated(class_analysis.extends):
            return 0
        return hash(class_analysis.extends)

    @classmethod
    def _get_string_literals_count(cls, class_analysis):
        return len(list(StringLiteralsExtractor.extract_strings(class_analysis)))

    @classmethod
    def _get_string_literals_simhash(cls, class_analysis):
        return calculate_simhash(
            StringLiteralsExtractor.extract_strings(class_analysis)
        )

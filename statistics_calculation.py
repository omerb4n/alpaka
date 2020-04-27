import json
from abc import ABCMeta
from argparse import ArgumentParser
from collections import defaultdict
from enum import Enum
from typing import Dict, Iterable

from androguard.misc import AnalyzeAPK
from simhash.simhash import num_differing_bits

from alpaka.apk.class_info import ClassInfo
from alpaka.class_signature.class_signature_calculator import ClassSignatureCalculator
from alpaka.class_signature.distance import SignatureDistanceCalculator
from alpaka.class_signature.signature import ClassSignature
from alpaka.obfuscation_detection.base import DummyObfuscationDetector


def main(apk1_path, apk2_path, result_path):
    used_parameters = [
        ('member_count', ParameterType.COUNT),
        ('method_count', ParameterType.COUNT),
        ('instructions_count', ParameterType.COUNT),
        ('members_simhash', ParameterType.SIMHASH),
        ('methods_params_simhash', ParameterType.SIMHASH),
        ('methods_returns_simhash', ParameterType.SIMHASH),
        ('instructions_simhash', ParameterType.SIMHASH),
        ('instruction_shingles_simhash', ParameterType.SIMHASH),
        ('implemented_interfaces_count', ParameterType.COUNT),
        ('implemented_interfaces_simhash', ParameterType.SIMHASH),
        ('superclass_hash', ParameterType.HASH),
        ('string_literals_count', ParameterType.COUNT),
        ('string_literals_simhash', ParameterType.SIMHASH),
    ]
    result = ParameterStatisticsCalculator(used_parameters).calculate_statistics_for_apks(apk1_path, apk2_path)
    with open(result_path, 'w') as result_file:
        json.dump(result, result_file, indent=4)


class ParameterStatisticsCalculator:

    def __init__(self, used_parameters):
        self._used_parameters = used_parameters

    def calculate_statistics_for_apks(self, apk1_path, apk2_path):
        signature_calculator = ClassSignatureCalculator(DummyObfuscationDetector())
        apk1_classes = {
            class_analysis.name: class_info
            for class_analysis in AnalyzeAPK(apk1_path)[2].get_classes()
            if not (class_info := ClassInfo(class_analysis, False, signature_calculator)).analysis.is_external()
            and not class_info.analysis.name.startswith('Landroid/')
        }
        apk2_classes = {
            class_analysis.name: class_info
            for class_analysis in AnalyzeAPK(apk2_path)[2].get_classes()
            if not (class_info := ClassInfo(class_analysis, False, signature_calculator)).analysis.is_external()
            and not class_info.analysis.name.startswith('Landroid/')
        }
        return {
            parameter_name:
                self._calculate_statistics_for_parameter(parameter_name, parameter_type, apk1_classes, apk2_classes)
            for parameter_name, parameter_type in self._used_parameters
        }

    @classmethod
    def _calculate_statistics_for_parameter(cls, parameter_name, parameter_type, apk1_classes, apk2_classes):
        parameter_distance_calculator = SingleParameterDistanceCalculator(parameter_name, parameter_type)
        distance_statistics_calculator = DistanceStatisticsCalculator(parameter_distance_calculator)
        return distance_statistics_calculator.calculate_distance_statistics(apk1_classes.values(), apk2_classes)


class DistanceStatisticsCalculator:

    def __init__(self, distance_calculator: SignatureDistanceCalculator):
        self._distance_calculator = distance_calculator

    def calculate_distance_statistics(self, apk1_classes: Iterable[ClassInfo], apk2_classes: Dict[str, ClassInfo]):
        results = dict()
        for apk1_class in apk1_classes:
            distance_counts = self._calculate_distance_counts_for_class(apk1_class.signature, apk2_classes.values())
            class_name = apk1_class.analysis.name
            matching_class = apk2_classes.get(class_name)
            if matching_class is not None:
                matching_class_distance = self._distance_calculator.distance(apk1_class.signature, matching_class.signature)
                results[class_name] = (distance_counts, matching_class_distance)
            else:
                results[class_name] = (distance_counts, None)
        return results

    def _calculate_distance_counts_for_class(self, class_signature, compared_classes):
        results = defaultdict(int)
        for compared_class in compared_classes:
            distance = self._distance_calculator.distance(class_signature, compared_class.signature)
            results[distance] += 1
        return results


class ParameterType(Enum):
    COUNT = 'count'
    SIMHASH = 'simhash'
    HASH = 'hash'


class SingleParameterDistanceCalculator(SignatureDistanceCalculator, metaclass=ABCMeta):

    def __init__(self, parameter_name, parameter_type):
        self._parameter_name = parameter_name
        self._parameter_type = parameter_type

    def _get_parameter_value(self, sig: ClassSignature):
        return getattr(sig, self._parameter_name)

    def distance(self, sig1: ClassSignature, sig2: ClassSignature) -> float:
        if self._parameter_type is ParameterType.COUNT:
            return abs(self._get_parameter_value(sig1) - self._get_parameter_value(sig2))
        if self._parameter_type is ParameterType.SIMHASH:
            return num_differing_bits(self._get_parameter_value(sig1), self._get_parameter_value(sig2))
        if self._parameter_type is ParameterType.HASH:
            return 1 if self._get_parameter_value(sig1) != self._get_parameter_value(sig2) else 0


if __name__ == '__main__':
    parser = ArgumentParser(description='calculate signature parameter statistics for 2 apks')
    parser.add_argument('apk1_path')
    parser.add_argument('apk2_path')
    parser.add_argument('result_path')
    args = parser.parse_args()
    main(args.apk1_path, args.apk2_path, args.result_path)

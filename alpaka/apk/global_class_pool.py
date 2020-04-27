from collections import defaultdict
from typing import Dict

from androguard.core.analysis.analysis import ClassAnalysis

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.class_info import ClassInfo
from alpaka.apk.package_info import PackageInfo, PackagePool
from alpaka.apk.class_pool import ClassPool
from alpaka.class_signature.class_signature_calculator import ClassSignatureCalculator
from alpaka.obfuscation_detection.base import ObfuscationDetector
from alpaka.utils import DictFilterMixin


class GlobalClassPool(ClassPool, DictFilterMixin, Dict[str, ClassInfo]):
    """
    A class pool containing all of the classes relevant to the comparison from a single apk
    """

    def __init__(
            self,
            analyzed_apk: AnalyzedApk,
            obfuscation_detector: ObfuscationDetector,
            signature_calculator: ClassSignatureCalculator
    ):
        self._obfuscation_detector: ObfuscationDetector = obfuscation_detector
        self._signature_calculator = signature_calculator
        super(GlobalClassPool, self).__init__({
            class_name: self._create_class_info(class_analysis)
            for class_name, class_analysis in analyzed_apk.analysis.classes.items()
            if not class_analysis.is_external()
        })

    def split_by_package(self) -> PackagePool:
        packages_dict = dict()
        for class_name, class_info in self.items():
            package_name_prefix = PackageInfo.get_parent_package_name_prefix(class_name)
            if package_name_prefix not in packages_dict:
                packages_dict[package_name_prefix] = self._create_package_info(package_name_prefix)
            packages_dict[package_name_prefix].add_class(class_info)
        return packages_dict

    def _create_package_info(self, package_name_prefix) -> PackageInfo:
        """
        Initializes a PackageInfo instance,
        Using the instance's package name obfuscation detector to determine if the name is obfuscated
        """
        is_obfuscated_name = self._obfuscation_detector.is_package_name_obfuscated(package_name_prefix)
        return PackageInfo(package_name_prefix, is_obfuscated_name)

    def _create_class_info(self, class_analysis: ClassAnalysis) -> ClassInfo:
        """
        Initializes a ClassInfo instance,
        Using the instance's class name obfuscation detector to determine if the name is obfuscated
        """
        is_obfuscated_name = self._obfuscation_detector.is_class_name_obfuscated(class_analysis.name)
        return ClassInfo(class_analysis, is_obfuscated_name, self._signature_calculator)

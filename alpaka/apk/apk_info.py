from typing import Dict

from androguard.core.analysis.analysis import ClassAnalysis

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.class_info import ClassInfo
from alpaka.apk.package_info import PackageInfo
from alpaka.apk.config import ROOT_PACKAGE
from alpaka.obfuscation.obfuscation import PackageNameObfuscationDetector, ClassNameObfuscationDetector
from alpaka.utils import filter_dict

PackagesDict = Dict[str, PackageInfo]


class ApkInfo:
    """
    Holds and manipulates information about the apk's packages, classes etc.
    """

    def __init__(self, analyzed_apk: AnalyzedApk, assume_obfuscated: bool = True,
                 use_obfuscation_detectors: bool = True):
        self._analyzed_apk = analyzed_apk
        self._assume_obfuscated = assume_obfuscated
        self._use_obfuscation_detectors = use_obfuscation_detectors
        self._classes = self._analyzed_apk.analysis.classes
        self._packages_dict: PackagesDict = None

        self._package_name_obfuscation_detector = PackageNameObfuscationDetector()
        self._class_name_obfuscation_detector = ClassNameObfuscationDetector()

    def filter_classes(self, class_filter):
        self._classes = filter_dict(self._analyzed_apk.analysis.classes, class_filter)

    def pack(self):
        self._packages_dict = {}
        for class_analysis in self._classes.values():
            package_name_prefix = PackageInfo.get_parent_package_name_prefix(class_analysis.name)
            if package_name_prefix not in self._packages_dict:
                self._add_package(package_name_prefix)
            class_info = self._create_class_info(class_analysis)
            self._packages_dict[package_name_prefix].add_class(class_info)

    def _add_package(self, package_name_prefix):
        self._packages_dict[package_name_prefix] = self._create_package_info(package_name_prefix)

    def _create_package_info(self, package_name_prefix) -> PackageInfo:
        is_obfuscated_name = self._assume_obfuscated
        if self._use_obfuscation_detectors:
            package_name = PackageInfo.get_package_name(package_name_prefix)
            is_obfuscated_name = self._package_name_obfuscation_detector.is_obfuscated(package_name)
        return PackageInfo(package_name_prefix, is_obfuscated_name)

    def _create_class_info(self, class_analysis: ClassAnalysis) -> ClassInfo:
        is_obfuscated_name = self._assume_obfuscated
        if self._use_obfuscation_detectors:
            class_name = ClassInfo.get_class_name(class_analysis.name)
            is_obfuscated_name = self._class_name_obfuscation_detector.is_obfuscated(class_name)
        return ClassInfo(class_analysis, is_obfuscated_name)

    @property
    def packages_dict(self) -> PackagesDict:
        if self._packages_dict:
            return self._packages_dict
        else:
            self._packages_dict = {
                ROOT_PACKAGE: PackageInfo(ROOT_PACKAGE, False,
                                          {class_analysis.name: self._create_class_info(class_analysis) for
                                           class_analysis in self._classes})}
            return self._packages_dict

    def generate_parent_packages_dict(self, package_name_prefix) -> dict:
        parent_packages_dict = {}
        if package_name_prefix in self._packages_dict:
            parent_package_name_prefix = PackageInfo.get_parent_package_name_prefix(package_name_prefix)
            for another_package_name_prefix in self._packages_dict:
                if PackageInfo.get_parent_package_name_prefix(
                        another_package_name_prefix) == parent_package_name_prefix:
                    # Make sure it's not the same package
                    if another_package_name_prefix is not package_name_prefix:
                        parent_packages_dict[another_package_name_prefix] = self._packages_dict[
                            another_package_name_prefix]
        return parent_packages_dict

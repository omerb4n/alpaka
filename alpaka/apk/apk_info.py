from typing import List

from androguard.core.analysis.analysis import ClassAnalysis

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.class_info import ClassInfo
from alpaka.apk.package_info import PackageInfo, ROOT_PACKAGE
from alpaka.obfuscation.obfuscation import PackageNameObfuscationDetector, ClassNameObfuscationDetector
from alpaka.utils import filter_dict


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
        self._packages: dict = None

        self._package_name_obfuscation_detector = PackageNameObfuscationDetector()
        self._class_name_obfuscation_detector = ClassNameObfuscationDetector()

    def filter_classes(self, class_filter):
        self._classes = filter_dict(self._analyzed_apk.analysis.classes, class_filter)

    def pack(self):
        self._packages = {}
        for class_analysis in self._classes.values():
            package_name_prefix = PackageInfo.get_parent_package_name_prefix(class_analysis.name)
            if package_name_prefix not in self._packages:
                self._add_package(package_name_prefix)
            class_info = self._create_class_info(class_analysis)
            self._packages[package_name_prefix].add_class(class_info)

    def _add_package(self, package_name_prefix):
        self._packages[package_name_prefix] = self._create_package_info(package_name_prefix)

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

    def get_packages(self, is_obfuscated: bool = None, is_matched: bool = None) -> List[PackageInfo]:
        packages = self._get_packages()
        for package in packages.values():
            if is_obfuscated is not None and package.is_obfuscated_name != is_obfuscated:
                continue
            if is_matched is not None and (package.get_match() is not None) != is_matched:
                continue
            yield package

    def _get_packages(self) -> dict:
        if self._packages:
            return self._packages
        else:
            return {ROOT_PACKAGE: PackageInfo(ROOT_PACKAGE, False, self._classes)}

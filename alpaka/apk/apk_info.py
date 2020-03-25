from typing import Optional, List

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.package_info import PackageInfo, ROOT_PACKAGE
from alpaka.obfuscation.obfuscation import PackageNameObfuscationDetector
from alpaka.utils import filter_dict


class ApkInfo:
    def __init__(self, analyzed_apk: AnalyzedApk, assume_obfuscated: bool = True,
                 use_obfuscation_detectors: bool = True):
        self._analyzed_apk = analyzed_apk
        self._assume_obfuscated = assume_obfuscated
        self._use_obfuscation_detectors = use_obfuscation_detectors
        self._classes = self._analyzed_apk.analysis.classes
        self._packages: Optional[List[PackageInfo]] = None

        self._package_name_obfuscation_detector = PackageNameObfuscationDetector()

    def filter_classes(self, class_filter):
        self._classes = filter_dict(self._analyzed_apk.analysis.classes, class_filter)

    def pack(self):
        self._packages = {}
        for class_analysis in self._classes.values():
            package_name_prefix = PackageInfo.get_parent_package_name_prefix(class_analysis.name)
            if package_name_prefix not in self._packages:
                self._add_package(package_name_prefix)
            self._packages[package_name_prefix].add_class(class_analysis.name)

    def _add_package(self, package_name_prefix):
        is_obfuscated_name = self._assume_obfuscated
        if self._use_obfuscation_detectors:
            package_name = PackageInfo.get_package_name(package_name_prefix)
            is_obfuscated_name = self._package_name_obfuscation_detector.is_obfuscated(package_name)
        self._packages[package_name_prefix] = PackageInfo(package_name_prefix, is_obfuscated_name)

    def get_packages(self):
        if self._packages:
            return self._packages
        else:
            return {ROOT_PACKAGE: self._classes}

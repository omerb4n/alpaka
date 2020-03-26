from typing import Optional, List

from alpaka.analyzed_apk import AnalyzedApk
from alpaka.obfuscation.obfuscation import PackageNameObfuscationDetector
from alpaka.utils import filter_dict


class PackageInfo:
    NAME_SEPARATOR = '/'

    def __init__(self, package_name_prefix: str, is_obfuscated_name):
        self.name_prefix = package_name_prefix
        self.classes = []
        self.is_obfuscated_name = is_obfuscated_name

    def add_class(self, class_name: str):
        self.classes.append(class_name)

    def get_classes(self):
        return self.classes

    @staticmethod
    def get_parent_package_name_prefix(package_name_prefix):
        return package_name_prefix[:package_name_prefix.rfind(PackageInfo.NAME_SEPARATOR)]

    @staticmethod
    def get_package_name(package_name_prefix):
        return package_name_prefix[package_name_prefix.rfind(PackageInfo.NAME_SEPARATOR)+1:]

    def __repr__(self):
        return "~Obfuscated" if self.is_obfuscated_name else ""


class ApkInfo:
    def __init__(self, analyzed_apk: AnalyzedApk):
        self._analyzed_apk = analyzed_apk
        self._classes = self._analyzed_apk.analysis.classes
        self._packages: Optional[List[PackageInfo]] = None

    def filter_classes(self, class_filter):
        self._classes = filter_dict(self._analyzed_apk.analysis.classes, class_filter)

    def pack(self):
        self._packages = {}
        package_name_obfuscation_detector = PackageNameObfuscationDetector()
        for class_analysis in self._classes.values():
            package_name_prefix = PackageInfo.get_parent_package_name_prefix(class_analysis.name)
            package_name = PackageInfo.get_package_name(package_name_prefix)
            if package_name_prefix not in self._packages:
                is_obfuscated = False
                if package_name_obfuscation_detector.is_obfuscated(package_name):
                    is_obfuscated = True
                self._packages[package_name_prefix] = PackageInfo(package_name_prefix, is_obfuscated)
            self._packages[package_name_prefix].add_class(class_analysis.name)

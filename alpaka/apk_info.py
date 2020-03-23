from typing import Optional, List

from alpaka.analyzed_apk import AnalyzedApk
from alpaka.utils import filter_dict


class PackageInfo:
    def __init__(self, name: str):
        self.name = name
        self._classes = []

    def add_class(self, class_name: str):
        self._classes.append(class_name)

    def get_classes(self):
        return self._classes

    @staticmethod
    def get_package_name(class_name):
        return class_name[:class_name.rfind('/')]


class ApkInfo:
    def __init__(self, analyzed_apk: AnalyzedApk):
        self._analyzed_apk = analyzed_apk
        self._classes = self._analyzed_apk.analysis.classes
        self._packages: Optional[List[PackageInfo]] = None

    def filter_classes(self, class_filter):
        self._classes = filter_dict(self._analyzed_apk.analysis.classes, class_filter)

    def pack(self):
        self._packages = {}
        for class_name, class_analysis in self._classes.items():
            package_name = PackageInfo.get_package_name(class_analysis.name)
            if package_name not in self._packages:
                self._packages[package_name] = PackageInfo(package_name)
            self._packages[package_name].add_class(class_name)

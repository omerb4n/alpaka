from typing import Dict, Optional

from androguard.core.analysis.analysis import ClassAnalysis

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.class_info import ClassInfo
from alpaka.apk.package_info import PackageInfo
from alpaka.apk.config import ROOT_PACKAGE
from alpaka.obfuscation_detection.score_based_detection import ObfuscationDetector
from alpaka.utils import filter_dict

PackagesDict = Dict[str, PackageInfo]


class ApkInfo:
    """
    Holds and manipulates information about the apk, apk's packages, classes etc.
    """

    def __init__(self, analyzed_apk: AnalyzedApk,
                 package_name_obfuscation_detector: ObfuscationDetector,
                 class_name_obfuscation_detector: ObfuscationDetector):
        self._analyzed_apk = analyzed_apk
        self._classes = self._analyzed_apk.analysis.classes
        self._packages_dict: Optional[PackagesDict] = None

        self._package_name_obfuscation_detector: ObfuscationDetector = package_name_obfuscation_detector
        self._class_name_obfuscation_detector: ObfuscationDetector = class_name_obfuscation_detector

    def filter_classes(self, class_filter):
        """
        Overrides the classes dictionary with a filtered dictionary.
        :param class_filter: filter function
        """
        self._classes = filter_dict(self._analyzed_apk.analysis.classes, class_filter)

    def pack(self):
        """
        Generates a PackagesDict
        This is done by:
        1. iterating over all the classes in the apk info
        2. determining to which package they belong by the class's name
        3. Creating PackageInfo and ClassInfo instances for each class and package.
        4. Updating the instance's packages dictionary

        Overrides the instance's packages dict with the result.
        """
        self._packages_dict = {}
        for class_analysis in self._classes.values():
            if class_analysis.is_external():
                continue
            package_name_prefix = PackageInfo.get_parent_package_name_prefix(class_analysis.name)
            if package_name_prefix not in self._packages_dict:
                self._add_package(package_name_prefix)
            class_info = self._create_class_info(class_analysis)
            self._packages_dict[package_name_prefix].add_class(class_info)

    def _add_package(self, package_name_prefix):
        """
        Creates and adds the new PackageInfo to the instance's packages dictionary.
        """
        self._packages_dict[package_name_prefix] = self._create_package_info(package_name_prefix)

    def _create_package_info(self, package_name_prefix) -> PackageInfo:
        """
        Initializes a PackageInfo instance,
        Using the instance's package name obfuscation detector to determine if the name is obfuscated
        """
        is_obfuscated_name = self._package_name_obfuscation_detector.is_obfuscated(package_name_prefix)
        return PackageInfo(package_name_prefix, is_obfuscated_name)

    def _create_class_info(self, class_analysis: ClassAnalysis) -> ClassInfo:
        """
        Initializes a ClassInfo instance,
        Using the instance's class name obfuscation detector to determine if the name is obfuscated
        """
        is_obfuscated_name = self._class_name_obfuscation_detector.is_obfuscated(class_analysis.name)
        return ClassInfo(class_analysis, is_obfuscated_name)

    @property
    def packages_dict(self) -> PackagesDict:
        """
        If the packages dict exists return it.
        Else override the packages dictionary with a default package.

        The default package:
        * package name is the root package name.
        * By default flagged as obfuscated.
        * The package's classes will hold all the classes of the apk.
        """
        if not self._packages_dict:
            self._packages_dict = {
                ROOT_PACKAGE: PackageInfo(ROOT_PACKAGE, True,
                                          {class_analysis.name: self._create_class_info(class_analysis) for
                                           class_analysis in self._classes.values()})}
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

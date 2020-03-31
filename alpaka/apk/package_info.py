from __future__ import annotations

from typing import Dict

from alpaka.apk.class_info import ClassInfo
from alpaka.utils import get_domain_name, get_subdomain

ClassesDict = Dict[str, ClassInfo]


class PackageInfo:
    def __init__(self, package_name_prefix: str, is_obfuscated_name: bool, classes_dict: ClassesDict = None):
        self.name_prefix = package_name_prefix
        self.classes_dict: ClassesDict = {}
        if classes_dict:
            self.classes_dict = classes_dict
        self.is_obfuscated_name = is_obfuscated_name

    def add_class(self, class_info: ClassInfo):
        self.classes_dict[class_info.analysis.name] = class_info

    @staticmethod
    def get_parent_package_name_prefix(package_name_prefix):
        return get_subdomain(package_name_prefix)

    @staticmethod
    def get_package_name(package_name_prefix):
        return get_domain_name(package_name_prefix)

    def __repr__(self):
        return "~Obfuscated" if self.is_obfuscated_name else ""

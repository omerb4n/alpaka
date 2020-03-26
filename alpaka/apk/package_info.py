from __future__ import annotations
from typing import List

from alpaka.apk.class_info import ClassInfo
from alpaka.utils import get_domain_name, get_subdomain

ROOT_PACKAGE = ''


class PackageInfo:
    def __init__(self, package_name_prefix: str, is_obfuscated_name, classes: List[ClassInfo] = None):
        self.name_prefix = package_name_prefix
        self.classes = []
        if classes:
            self._classes = classes
        self.is_obfuscated_name = is_obfuscated_name
        self._match = None

    def add_class(self, class_info: ClassInfo):
        self.classes.append(class_info)

    def get_classes(self) -> List[ClassInfo]:
        return self.classes

    def _set_match(self, match_package_info: PackageInfo):
        self._match = match_package_info

    def get_match(self) -> PackageInfo:
        return self._match

    @staticmethod
    def get_parent_package_name_prefix(package_name_prefix):
        return get_subdomain(package_name_prefix)

    @staticmethod
    def get_package_name(package_name_prefix):
        return get_domain_name(package_name_prefix)

    def __repr__(self):
        return "~Obfuscated" if self.is_obfuscated_name else ""

    @staticmethod
    def match(a: PackageInfo, b: PackageInfo):
        a._set_match(a)
        b._set_match(b)

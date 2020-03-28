from __future__ import annotations
from typing import List

from alpaka.apk.class_info import ClassInfo
from alpaka.utils import get_domain_name, get_subdomain

ROOT_PACKAGE = ''


class PackageInfo:
    def __init__(self, package_name_prefix: str, is_obfuscated_name: bool, classes: List[ClassInfo] = None):
        self.name_prefix = package_name_prefix
        self._classes = []
        if classes:
            self._classes = classes
        self.is_obfuscated_name = is_obfuscated_name

    def add_class(self, class_info: ClassInfo):
        self._classes.append(class_info)

    def get_classes(self) -> List[ClassInfo]:
        return self._classes

    @staticmethod
    def get_parent_package_name_prefix(package_name_prefix):
        return get_subdomain(package_name_prefix)

    @staticmethod
    def get_package_name(package_name_prefix):
        return get_domain_name(package_name_prefix)

    def __repr__(self):
        return "~Obfuscated" if self.is_obfuscated_name else ""

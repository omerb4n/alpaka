from __future__ import annotations

from typing import Dict

from alpaka.apk.class_info import ClassInfo
from alpaka.apk.class_pool import ClassPool
from alpaka.constants import PACKAGE_NAME_SEPARATOR, CLASS_JAVA_KEYWORD
from alpaka.utils import get_domain_name, get_subdomain


class PackageInfo(ClassPool, Dict):
    """
    Holds and manipulates information about a package -
    """

    def __init__(self, package_name_prefix: str, is_obfuscated_name: bool, classes_dict: ClassPool = None):
        """

        :param package_name_prefix: full name of package (e.g. 'Lcom/example/myapplication')
        :param is_obfuscated_name: whether the package's name is obfuscated or not
        :param classes_dict: The package's classes.
        Should be a dictionary where the key is the class name and the value is a ClassInfo object
        """
        super(PackageInfo, self).__init__(classes_dict)
        self.name_prefix = package_name_prefix
        self.is_obfuscated_name = is_obfuscated_name

    def add_class(self, class_info: ClassInfo):
        """
        Adds the given ClassInfo to the classes_dict
        :param class_info:
        """
        self[class_info.analysis.name] = class_info

    @staticmethod
    def get_parent_package_name_prefix(package_name_prefix) -> str:
        """
        get the parent package name prefix of the given package_name_prefix.
        e.g. "Lcom/example/myapplication" -> "Lcom/example"
        """
        return get_subdomain(package_name_prefix)

    @staticmethod
    def get_package_name(package_name_prefix) -> str:
        """
        Get the package name (without prefix) of the given package_name_prefix
        e.g. "Lcom/example/myapplication" -> "myapplication"
        """
        if PACKAGE_NAME_SEPARATOR in package_name_prefix:
            return get_domain_name(package_name_prefix)
        else:
            return package_name_prefix[package_name_prefix.find(CLASS_JAVA_KEYWORD) + 1:]

    def __repr__(self):
        return "~Obfuscated" if self.is_obfuscated_name else ""


PackagePool = Dict[str, PackageInfo]

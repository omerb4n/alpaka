import itertools
from typing import Generator

from alpaka.apk.apk_info import ApkInfo
from alpaka.matchers.classes_pool_match import ClassesPoolMatch
from alpaka.apk.package_info import PackageInfo


class ClassesPoolMatcher:
    def __init__(self, old_apk_info: ApkInfo, new_apk_info: ApkInfo):
        # Shallow copies
        self._old_packages_dict: dict = dict(old_apk_info.packages_dict)
        self._new_packages_dict: dict = dict(new_apk_info.packages_dict)

    def pop_matched_packages_classes_pools(self) -> Generator[ClassesPoolMatch, None, None]:
        for package_key in self._old_packages_dict.keys():
            new_apk_package: PackageInfo = self._new_packages_dict.get(package_key)
            if new_apk_package is not None:
                if new_apk_package.is_obfuscated_name is False:
                    # For efficiency delete the packages from the local packages dicts
                    old_package = self._old_packages_dict.pop(package_key)
                    del self._new_packages_dict[package_key]
                    yield ClassesPoolMatch(old_package.get_classes(), new_apk_package.get_classes())

    def get_all_classes_pool(self) -> ClassesPoolMatch:
        old_apk_classes = list(
            itertools.chain.from_iterable([package.get_classes() for package in self._old_packages_dict]))
        new_apk_classes = list(
            itertools.chain.from_iterable([package.get_classes() for package in self._new_packages_dict]))
        return ClassesPoolMatch(old_apk_classes, new_apk_classes)

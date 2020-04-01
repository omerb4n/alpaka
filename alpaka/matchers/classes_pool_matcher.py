from collections import ChainMap
from typing import Generator

from alpaka.apk.apk_info import ApkInfo, PackagesDict
from alpaka.matchers.classes_pool_match import ClassesPoolMatch


class ClassesPoolMatcher:
    def __init__(self, old_apk_info: ApkInfo, new_apk_info: ApkInfo):
        # Shallow copies
        self._old_packages_dict: PackagesDict = dict(old_apk_info.packages_dict)
        self._new_packages_dict: PackagesDict = dict(new_apk_info.packages_dict)

    def pop_matched_packages_classes_pools(self) -> Generator[ClassesPoolMatch, None, None]:
        # For efficiency always use pop_matched_packages_classes_pools first
        for package_key in list(self._old_packages_dict.keys()):
            new_apk_package = self._new_packages_dict.get(package_key)
            if new_apk_package is not None:
                if new_apk_package.is_obfuscated_name is False:
                    # For efficiency delete the packages from the local packages dicts
                    old_package = self._old_packages_dict.pop(package_key)
                    del self._new_packages_dict[package_key]
                    yield ClassesPoolMatch(dict(old_package.classes_dict),
                                           dict(new_apk_package.classes_dict))

    def get_all_classes_pool_chain_map(self) -> ClassesPoolMatch:
        """
        For efficiency, each classes pool is a ChainMap.
        You should not remove elements or make any changes to this ChainMap.
        Changes will actually change the original dictionaries.
        :return:
        """
        old_classes_chain_map = ChainMap(*self.all_classes_dicts_iter(self._old_packages_dict))
        new_classes_chain_map = ChainMap(*self.all_classes_dicts_iter(self._old_packages_dict))
        return ClassesPoolMatch(old_classes_chain_map, new_classes_chain_map)

    @staticmethod
    def all_classes_dicts_iter(packages_dict: PackagesDict):
        # Don't create a shallow copy dict for efficiency
        return (package.classes_dict for package in packages_dict.values())

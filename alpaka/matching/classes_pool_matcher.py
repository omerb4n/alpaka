from collections import ChainMap
from typing import Generator

from alpaka.apk.class_pool import GlobalClassPool, PackagesDict, ClassPool
from alpaka.matching.classes_pool_match import ClassesPoolMatch


class ClassesPoolMatcher:
    """
    Responsible for dividing the given apks's classes to pools that have a matching pool in the other apk
    and exporting those matches

    A class pool is just a group of classes.
    Class pools are used to make actions like class matching more efficient.
    How? If we assume classes are in the same package in both apks,
    it is probably best to try to match only the package's classes.
    """

    def __init__(self, old_class_pool: GlobalClassPool, new_class_pool: GlobalClassPool):
        # Shallow copies
        self._old_packages_dict: PackagesDict = dict(old_class_pool.split_by_package())
        self._new_packages_dict: PackagesDict = dict(new_class_pool.split_by_package())

    def pop_matched_packages_classes_pools(self) -> Generator[ClassesPoolMatch, None, None]:
        """
        Tries to find packages with the same name in both apks.
        If such a pair is found:
            * For efficiency, Remove the package from the packages dict, because no other match should be made with it
            * Initialize ClassesPoolMatch with the packages's classes and yield it

        For efficiency always use pop_matched_packages_classes_pools first
        :return: Returns a generator for ClassesPoolMatch
        """
        for package_key in list(self._old_packages_dict.keys()):
            new_apk_package = self._new_packages_dict.get(package_key)
            if new_apk_package is not None:
                if new_apk_package.is_obfuscated_name is False:
                    # For efficiency delete the packages from the local packages dicts
                    old_package = self._old_packages_dict.pop(package_key)
                    del self._new_packages_dict[package_key]
                    yield ClassesPoolMatch(dict(old_package), dict(new_apk_package))

    def get_all_classes_pool_chain_map(self) -> ClassesPoolMatch:
        """
        Returns pools that hold all the remaining classes.

        For efficiency, each classes pool is a ChainMap.
        You should not remove elements or make any changes to this ChainMap.
        Changes will actually change the original dictionaries.
        :return: ClassesPoolMatch with pools that hold all the remaining classes
        """
        old_classes_chain_map = ChainMap(*self._old_packages_dict.values())
        new_classes_chain_map = ChainMap(*self._new_packages_dict.values())
        return ClassesPoolMatch(old_classes_chain_map, new_classes_chain_map)

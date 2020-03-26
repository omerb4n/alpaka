from typing import List, Generator

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.apk_info import ApkInfo
from alpaka.apk.package_info import PackageInfo
from alpaka.apk.classes_pool import ClassesPool


class ApkDiffer:
    """
    Diffs between two AnalyzedApks using ApkInfo
    """

    def __init__(self, old_apk: AnalyzedApk, new_apk: AnalyzedApk):
        self._old_apk_info = ApkInfo(old_apk)
        self._new_apk_info = ApkInfo(new_apk)

    def filter_classes(self, class_filter):
        self._old_apk_info.filter_classes(class_filter)
        self._new_apk_info.filter_classes(class_filter)

    def pack(self):
        self._old_apk_info.pack()
        self._new_apk_info.pack()

    def _get_classes_pools_iterator(self) -> Generator[ClassesPool, None, None]:
        yield self._get_classes_pools_from_not_obfuscated_packages()

    def _get_classes_pools_from_not_obfuscated_packages(self) -> Generator[ClassesPool, None, None]:
        old_apk_packages = self._old_apk_info.get_packages_dict_items_iterator(is_obfuscated=False)
        new_apk_packages: dict = self._new_apk_info.get_packages_dict()
        for old_apk_package_name_prefix, old_apk_package in old_apk_packages:
            new_apk_package: PackageInfo = new_apk_packages.get(old_apk_package_name_prefix)
            if new_apk_package is not None and new_apk_package.is_obfuscated_name is False:
                yield ClassesPool(old_apk_package.get_classes(), new_apk_package.get_classes())

    def find_class_matches(self):
        for classes_pool in self._get_classes_pools_iterator():
            for class_info in classes_pool.old_classes:
                # TODO: check if obfuscated and try to match
                pass

    def generate_class_signature(self):
        pass

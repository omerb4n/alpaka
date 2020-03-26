from typing import List

from alpaka.apk import packages_match
from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.apk_info import ApkInfo
from alpaka.apk.package_info import PackageInfo
from alpaka.apk.packages_match import ClassesPool


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

    def _get_classes_pools(self) -> List[ClassesPool]:
        classes_pools: List[ClassesPool] = []
        # TODO change get_packages to return dict
        old_apk_packages: List[PackageInfo] = self._old_apk_info.get_packages(is_obfuscated=False)
        new_apk_packages: List[PackageInfo] = list(self._new_apk_info.get_packages(is_obfuscated=False))
        for old_apk_package in old_apk_packages:
            for new_apk_package in new_apk_packages:
                if old_apk_package.name_prefix == new_apk_package.name_prefix:
                    classes_pools.append(ClassesPool(old_apk_package.get_classes(), new_apk_package.get_classes()))
        return classes_pools

    def find_class_matches(self):
        classes_pools: List[ClassesPool] = self._get_classes_pools()
        for classes_pool in classes_pools:
            for class_info in classes_pool.old_classes:
                # TODO: check if obfuscated and try to match
                pass

    def generate_class_signature(self):
        pass

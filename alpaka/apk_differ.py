from typing import List

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.apk_info import ApkInfo
from alpaka.apk.package_info import PackageInfo


class ApkDiffer:
    def __init__(self, old_apk: AnalyzedApk, new_apk: AnalyzedApk):
        self._old_apk_info = ApkInfo(old_apk)
        self._new_apk_info = ApkInfo(new_apk)

    def filter_classes(self, class_filter):
        self._old_apk_info.filter_classes(class_filter)
        self._new_apk_info.filter_classes(class_filter)

    def pack(self):
        self._old_apk_info.pack()
        self._new_apk_info.pack()
        self._match_packages()

    def _match_packages(self):
        # TODO change to dict
        old_apk_packages: List[PackageInfo] = self._old_apk_info.get_packages(is_obfuscated=False)
        new_apk_packages: List[PackageInfo] = list(self._new_apk_info.get_packages(is_obfuscated=False))
        for old_apk_package in old_apk_packages:
            for new_apk_package in new_apk_packages:
                if old_apk_package.name_prefix == new_apk_package.name_prefix:
                    PackageInfo.match(old_apk_package, new_apk_package)
                    # For efficiency
                    new_apk_packages.remove(new_apk_package)

    def _get_matched_packages_classes(self) -> tuple:
        matched_old_apk_packages: List[PackageInfo] = self._old_apk_info.get_packages(is_matched=True)
        for matched_old_apk_package in matched_old_apk_packages:
            matched_new_apk_package = matched_old_apk_package.get_match()
            yield (matched_old_apk_package.get_classes(), matched_new_apk_package.get_classes())

    def match_classes(self):
        pass

    def generate_class_signature(self):
        pass

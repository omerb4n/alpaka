import itertools
from typing import Generator, List

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.apk_info import ApkInfo
from alpaka.apk.class_info import ClassInfo
from alpaka.apk.class_matches import ClassMatches, ClassMatch
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
        not_obfuscated_packages_classes_pools_iterator = self._get_not_obfuscated_packages_classes_pools()
        obfuscated_packages_classes_pools_iterator = self._get_obfuscated_packages_classes_pool()
        for classes_pool in not_obfuscated_packages_classes_pools_iterator:
            yield classes_pool
        for classes_pool in obfuscated_packages_classes_pools_iterator:
            yield classes_pool

    def _get_not_obfuscated_packages_classes_pools(self) -> Generator[ClassesPool, None, None]:
        old_apk_packages = self._old_apk_info.get_packages_iterator(is_obfuscated=False)
        new_apk_packages: dict = self._new_apk_info.get_packages_dict()
        for old_apk_package in old_apk_packages:
            new_apk_package: PackageInfo = new_apk_packages.get(old_apk_package.name_prefix)
            if new_apk_package is not None and new_apk_package.is_obfuscated_name is False:
                yield ClassesPool(old_apk_package.get_classes(), new_apk_package.get_classes())

    def _get_obfuscated_packages_classes_pool(self) -> Generator[ClassesPool, None, None]:
        old_apk_packages = self._old_apk_info.get_packages_iterator(is_obfuscated=True)
        new_apk_packages = self._new_apk_info.get_packages_iterator(is_obfuscated=True)
        old_apk_classes = list(itertools.chain.from_iterable([package.get_classes() for package in old_apk_packages]))
        new_apk_classes = list(itertools.chain.from_iterable([package.get_classes() for package in new_apk_packages]))
        yield ClassesPool(old_apk_classes, new_apk_classes)

    def find_classes_matches(self) -> List[ClassMatches]:
        classes_matches: List[ClassMatches] = []
        for classes_pool in self._get_classes_pools_iterator():
            for class_info in classes_pool.old_classes:
                if class_info.is_obfuscated_name:
                    # TODO: uncomment the line bellow
                    # classes_matches.append(self._find_class_matches_by_signature(class_info, classes_pool.new_classes))
                    pass
                else:
                    classes_matches.append(
                        self._find_class_matches_by_name(class_info, classes_pool.new_classes))
        return classes_matches

    def _find_class_matches_by_signature(self, class_to_match: ClassInfo,
                                         potential_matches: List[ClassInfo]) -> ClassMatches:
        # TODO: Use ClassSignature distances
        raise NotImplementedError()

    def _find_class_matches_by_name(self, class_to_match: ClassInfo,
                                    potential_matches: List[ClassInfo]) -> ClassMatches:
        # TODO: Maybe change ClassesPool.new_classes to be a dict
        #  so that finding the same class name will be more efficient
        for potential_match in potential_matches:
            if class_to_match.analysis.name == potential_match.analysis.name:
                return ClassMatches(class_to_match, [ClassMatch(potential_match, 1.0)])
        return self._find_class_matches_by_signature(class_to_match, potential_matches)

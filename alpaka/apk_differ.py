from typing import Callable, Iterable, Optional, ChainMap

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.global_class_pool import GlobalClassPool
from alpaka.class_signature.class_signature_calculator import ClassSignatureCalculator
from alpaka.matching.class_matcher import ClassMatcher
from alpaka.matching.package_matcher import NameBasedPackageMatcher
from alpaka.obfuscation_detection.base import ObfuscationDetector


class ApkDiffer:
    """
    Diffs between two AnalyzedApks using ApkInfo and ClassMatcher
    """

    def __init__(
            self,
            obfuscation_detector: ObfuscationDetector,
            filters: Optional[Iterable[Callable]] = None,
    ):

        self._signature_calculator = ClassSignatureCalculator(obfuscation_detector)
        self._obfuscation_detector = obfuscation_detector
        self._filters = filters
        if filters is None:
            self._filters = []

    def diff(self, apk1: AnalyzedApk, apk2: AnalyzedApk, match_packages: bool = True, match_by_name: bool = True):
        class_pool1 = GlobalClassPool(apk1, self._obfuscation_detector, self._signature_calculator)
        class_pool2 = GlobalClassPool(apk2, self._obfuscation_detector, self._signature_calculator)
        for filter_func in self._filters:
            class_pool1.filter(filter_func)
            class_pool2.filter(filter_func)
        class_matcher = ClassMatcher()
        if not match_packages:
            return class_matcher.match(class_pool1, class_pool2).matches
        package_match_results = self._get_package_match_results(class_pool1, class_pool2)
        return self._get_class_matches_from_package_matches(class_matcher, match_by_name, package_match_results)

    @classmethod
    def _get_class_matches_from_package_matches(cls, class_matcher, match_by_name, package_match_results):
        class_matches = dict()
        for package_match in package_match_results.best_matches():
            class_match_results = class_matcher.match(package_match.item1, package_match.item2, match_by_name)
            class_matches.update(class_match_results.matches)
        remaining_classes1 = ChainMap(*package_match_results.unmatched[0].values())
        remaining_classes2 = ChainMap(*package_match_results.unmatched[1].values())
        class_match_results = class_matcher.match(remaining_classes1, remaining_classes2, False)
        class_matches.update(class_match_results.matches)
        return class_matches

    @classmethod
    def _get_package_match_results(cls, class_pool1, class_pool2):
        package_pool1 = class_pool1.split_by_package()
        package_pool2 = class_pool2.split_by_package()
        package_matcher = NameBasedPackageMatcher()
        return package_matcher.match(package_pool1, package_pool2)

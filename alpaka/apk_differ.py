from typing import Callable, Iterable, Optional

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.class_pool import GlobalClassPool
from alpaka.class_signature.class_signature_calculator import ClassSignatureCalculator
from alpaka.matching.class_matcher import ClassMatcher
from alpaka.obfuscation_detection.base import ObfuscationDetector


class ApkDiffer:
    """
    Diffs between two AnalyzedApks using ApkInfo and ClassMatcher
    """

    def __init__(
            self,
            package_name_obfuscation_detector: ObfuscationDetector,
            class_name_obfuscation_detector: ObfuscationDetector,
            filters: Optional[Iterable[Callable]] = None,
    ):

        self._signature_calculator = ClassSignatureCalculator(class_name_obfuscation_detector)
        self._class_name_obfuscation_detector = class_name_obfuscation_detector
        self._package_name_obfuscation_detector = package_name_obfuscation_detector
        self._filters = filters
        if filters is None:
            self._filters = []

    def diff(self, apk1: AnalyzedApk, apk2: AnalyzedApk):
        class_pool1 = GlobalClassPool(apk1, self._package_name_obfuscation_detector, self._class_name_obfuscation_detector, self._signature_calculator)
        class_pool2 = GlobalClassPool(apk2, self._package_name_obfuscation_detector, self._class_name_obfuscation_detector, self._signature_calculator)
        for filter_func in self._filters:
            class_pool1.filter(filter_func)
            class_pool2.filter(filter_func)
        class_matcher = ClassMatcher(class_pool1, class_pool2)
        return class_matcher.find_classes_matches()

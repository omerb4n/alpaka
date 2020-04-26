import json
from typing import Callable

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.apk_info import ApkInfo
from alpaka.class_signature.class_signature_calculator import ClassSignatureCalculator
from alpaka.encoders.classes_matches_encoder import ClassesMatchesEncoder
from alpaka.matchers.class_matcher import ClassMatcher
from alpaka.matchers.classes_matches import ClassesMatches
from alpaka.obfuscation_detection.base import ObfuscationDetector


class ApkDiffer:
    """
    Diffs between two AnalyzedApks using ApkInfo and ClassMatcher
    """

    def __init__(self, old_apk: AnalyzedApk, new_apk: AnalyzedApk,
                 package_name_obfuscation_detector: ObfuscationDetector,
                 class_name_obfuscation_detector: ObfuscationDetector):
        signature_calculator = ClassSignatureCalculator(class_name_obfuscation_detector)

        self._old_apk_info = ApkInfo(old_apk, package_name_obfuscation_detector, class_name_obfuscation_detector, signature_calculator)
        self._new_apk_info = ApkInfo(new_apk, package_name_obfuscation_detector, class_name_obfuscation_detector, signature_calculator)
        self._classes_matches: ClassesMatches = ClassesMatches()

    def filter_classes(self, class_filter: Callable):
        """
        Filter the classes for both apk infos
        Filtering your classes with only the relevant classes,
        should make other actions consume less time and resources and also more accurate.
        :param class_filter: Filter function
        """
        self._old_apk_info.filter_classes(class_filter)
        self._new_apk_info.filter_classes(class_filter)

    def pack(self):
        """
        Pack the classes for both apk infos.
        Packing can make the class matching process more efficient.
        """
        self._old_apk_info.pack()
        self._new_apk_info.pack()

    def find_classes_matches(self):
        """
        Use a ClassMatcher to to find the classes matches and hold the results in the classes matches field
        """
        class_matcher = ClassMatcher(self._old_apk_info, self._new_apk_info)
        self._classes_matches = class_matcher.find_classes_matches()

    # TODO: Move this to another class. Implement save and load functions
    def get_classes_matches_json(self, *args, **kwargs):
        return json.dumps(self._classes_matches, cls=ClassesMatchesEncoder, *args, **kwargs)

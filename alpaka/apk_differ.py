from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.apk_info import ApkInfo
from alpaka.matchers.class_matcher import ClassMatcher
from alpaka.obfuscation_detection.base import ObfuscationDetector


class ApkDiffer:
    """
    Diffs between two AnalyzedApks using ApkInfo
    """

    def __init__(self, old_apk: AnalyzedApk, new_apk: AnalyzedApk,
                 package_name_obfuscation_detector: ObfuscationDetector,
                 class_name_obfuscation_detector: ObfuscationDetector):
        self._old_apk_info = ApkInfo(old_apk, package_name_obfuscation_detector, class_name_obfuscation_detector)
        self._new_apk_info = ApkInfo(new_apk, package_name_obfuscation_detector, class_name_obfuscation_detector)

    def filter_classes(self, class_filter):
        self._old_apk_info.filter_classes(class_filter)
        self._new_apk_info.filter_classes(class_filter)

    def pack(self):
        self._old_apk_info.pack()
        self._new_apk_info.pack()

    def find_classes_matches(self):
        class_matcher = ClassMatcher(self._old_apk_info, self._new_apk_info)
        class_matcher.find_classes_matches()
        # TODO: This line is for POC, in practice some class should store the matches and give API to get and show them
        return class_matcher.class_matches

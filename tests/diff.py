from typing import Callable

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk_differ import ApkDiffer
from alpaka.obfuscation_detection.score_based_detection import ClassNameObfuscationDetector, \
    PackageNameObfuscationDetector
from tests.apks_config.apk_config import ApkConfig


def diff(old_apk_config: ApkConfig, new_apk_config: ApkConfig, class_filter: Callable = None):
    old_apk = AnalyzedApk(old_apk_config.apk_path, session_path=old_apk_config.session_path)
    new_apk = AnalyzedApk(new_apk_config.apk_path, session_path=new_apk_config.session_path)

    apk_differ = ApkDiffer(old_apk, new_apk, PackageNameObfuscationDetector(), ClassNameObfuscationDetector())
    if class_filter:
        apk_differ.filter_classes(class_filter)
    apk_differ.pack()
    apk_differ.find_classes_matches()
    print(apk_differ.get_classes_matches_json(indent=4))
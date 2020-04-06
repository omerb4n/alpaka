from androguard.core.analysis.analysis import ClassAnalysis

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk_differ import ApkDiffer
from alpaka.obfuscation.types import DummyObfuscationDetector
from tests.apks_config.facebook_262_0_0_34_117 import FACEBOOK_262_0_0_34_117_APK_CONFIG
from tests.apks_config.facebook_264_0_0_44_111 import FACEBOOK_264_0_0_44_111_APK_CONFIG
from tests.diff import diff


def filter_facebook_classes(class_name_prefix: str, _class_analysis: ClassAnalysis):
    for package in ['Lcom/facebook/pumpkin/', 'LX/']:
        if class_name_prefix.startswith(package) and not _class_analysis.is_external():
            return True
    return False


def test_facebook_apk():
    old_apk = AnalyzedApk(FACEBOOK_262_0_0_34_117_APK_CONFIG.apk_path, session_path=FACEBOOK_262_0_0_34_117_APK_CONFIG.session_path)
    new_apk = AnalyzedApk(FACEBOOK_264_0_0_44_111_APK_CONFIG.apk_path, session_path=FACEBOOK_264_0_0_44_111_APK_CONFIG.session_path)

    apk_differ = ApkDiffer(old_apk, new_apk, DummyObfuscationDetector(True), DummyObfuscationDetector(True))
    apk_differ.filter_classes(filter_facebook_classes)
    apk_differ.pack()
    print(apk_differ.find_classes_matches())
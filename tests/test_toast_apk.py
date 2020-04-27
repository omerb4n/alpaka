import json

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk_differ import ApkDiffer
from alpaka.encoders.classes_matches_encoder import ClassesMatchesEncoder
from alpaka.obfuscation_detection.score_based_detection import PackageNameObfuscationDetector, \
    ClassNameObfuscationDetector
from tests.apks_config.bye_apk_config import TOAST_BYE_APK_CONFIG
from tests.apks_config.hello_apk_config import TOAST_HELLO_APK_CONFIG
from tests.class_filters import android_class_filter


def test_toast_apk():
    old_apk = AnalyzedApk(TOAST_HELLO_APK_CONFIG.apk_path,
                          session_path=TOAST_HELLO_APK_CONFIG.session_path)
    new_apk = AnalyzedApk(TOAST_BYE_APK_CONFIG.apk_path,
                          session_path=TOAST_BYE_APK_CONFIG.session_path)

    apk_differ = ApkDiffer(PackageNameObfuscationDetector(), ClassNameObfuscationDetector(), [android_class_filter()])
    matches = apk_differ.diff(old_apk, new_apk)
    print(json.dumps(matches, cls=ClassesMatchesEncoder, indent=4))

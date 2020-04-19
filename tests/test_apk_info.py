from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.apk_info import ApkInfo
from alpaka.obfuscation_detection.base import DummyObfuscationDetector
from tests.apks_config.hello_apk_config import TOAST_HELLO_APK_CONFIG, MAIN_APPLICATION_PACKAGE, \
    MAIN_ACTIVIY
from tests.class_filters import android_class_filter


def test_apk_info():
    apk = ApkInfo(AnalyzedApk(TOAST_HELLO_APK_CONFIG.apk_path, session_path=TOAST_HELLO_APK_CONFIG.session_path),
                  DummyObfuscationDetector(False), DummyObfuscationDetector(True))
    apk.filter_classes(android_class_filter)
    apk.pack()
    assert apk.packages_dict[MAIN_APPLICATION_PACKAGE].classes_dict[MAIN_ACTIVIY]

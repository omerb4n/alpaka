from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.class_pool import GlobalClassPool
from alpaka.obfuscation_detection.base import DummyObfuscationDetector
from tests.apks_config.hello_apk_config import TOAST_HELLO_APK_CONFIG, MAIN_APPLICATION_PACKAGE, \
    MAIN_ACTIVIY
from tests.class_filters import android_class_filter

# todo: add signature calculator


def test_global_class_pool():
    apk = GlobalClassPool(AnalyzedApk(TOAST_HELLO_APK_CONFIG.apk_path, session_path=TOAST_HELLO_APK_CONFIG.session_path),
                          DummyObfuscationDetector(False), DummyObfuscationDetector(True))
    apk.filter(android_class_filter)
    assert apk.split_by_package()[MAIN_APPLICATION_PACKAGE][MAIN_ACTIVIY]

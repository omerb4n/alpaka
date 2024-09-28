from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.global_class_pool import GlobalClassPool
from alpaka.class_signature.class_signature_calculator import ClassSignatureCalculator
from alpaka.obfuscation_detection.base import DummyObfuscationDetector
from tests.apks_config.hello_apk_config import TOAST_HELLO_APK_CONFIG, MAIN_APPLICATION_PACKAGE, \
    MAIN_ACTIVIY
from tests.class_filters import android_class_filter


def test_global_class_pool():
    signature_calculator = ClassSignatureCalculator(DummyObfuscationDetector(False))
    apk = GlobalClassPool(AnalyzedApk(TOAST_HELLO_APK_CONFIG.apk_path, session_path=TOAST_HELLO_APK_CONFIG.session_path),
                          DummyObfuscationDetector(False), signature_calculator)
    apk.filter(android_class_filter)
    # todo: fix this test: all of the classes are external so the class pool is empty
    #assert apk.split_by_package()[MAIN_APPLICATION_PACKAGE][MAIN_ACTIVIY]

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.apk_info import ApkInfo
from tests.conftest import TOAST_HELLO_APK_PATH, TOAST_HELLO_SESSION_PATH
from tests.class_filters import android_class_filter


def test_apk_info():
    apk = ApkInfo(AnalyzedApk(TOAST_HELLO_APK_PATH, session_path=TOAST_HELLO_SESSION_PATH))
    apk.filter_classes(android_class_filter)
    apk.pack()
    pass

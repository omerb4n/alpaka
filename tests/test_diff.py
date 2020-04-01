from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk_differ import ApkDiffer
from tests.class_filters import android_class_filter
from tests.conftest import TOAST_HELLO_APK_PATH, TOAST_HELLO_SESSION_PATH, \
    TOAST_BYE_APK_PATH, TOAST_BYE_SESSION_PATH


def diff(old_apk_path, old_apk_session_path, new_apk_path, new_apk_session_path):
    old_apk = AnalyzedApk(old_apk_path, session_path=old_apk_session_path)
    new_apk = AnalyzedApk(new_apk_path, session_path=new_apk_session_path)

    apk_differ = ApkDiffer(old_apk, new_apk)
    apk_differ.filter_classes(android_class_filter)
    apk_differ.pack()
    apk_differ.find_classes_matches()
    pass


def test_toast_apk():
    diff(TOAST_HELLO_APK_PATH, TOAST_HELLO_SESSION_PATH, TOAST_BYE_APK_PATH, TOAST_BYE_SESSION_PATH)

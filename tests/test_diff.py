from alpaka.analyzed_apk import AnalyzedApk
from alpaka.apk_differ import ApkDiffer
from alpaka.apk_info import ApkInfo
from tests.conftest import TOAST_HELLO_APK_PATH, TOAST_HELLO_SESSION_PATH, \
    TOAST_BYE_APK_PATH, TOAST_BYE_SESSION_PATH


def my_filter(k: str, v):
    if k.startswith('Lcom/example/myapplication'):
        return True
    return False


def diff(old_apk_path, old_apk_session_path, new_apk_path, new_apk_session_path):
    old_apk = AnalyzedApk(old_apk_path, session_path=old_apk_session_path)
    new_apk = AnalyzedApk(new_apk_path, session_path=new_apk_session_path)

    apk_differ = ApkDiffer(old_apk, new_apk)
    # apk_differ.filter_classes(my_filter)
    apk_differ.pack()
    pass


def test_apk_info():
    apk = ApkInfo(AnalyzedApk(TOAST_HELLO_APK_PATH, session_path=TOAST_HELLO_SESSION_PATH))
    apk.pack()
    pass


def test_toast_apk():
    diff(TOAST_HELLO_APK_PATH, TOAST_HELLO_SESSION_PATH, TOAST_BYE_APK_PATH, TOAST_BYE_SESSION_PATH)

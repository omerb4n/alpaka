from androguard.core.analysis.analysis import ClassAnalysis

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.apk_info import ApkInfo
from alpaka.apk_differ import ApkDiffer
from tests.conftest import TOAST_HELLO_APK_PATH, TOAST_HELLO_SESSION_PATH, \
    TOAST_BYE_APK_PATH, TOAST_BYE_SESSION_PATH


def myapplication_filter(k: str, v):
    if k.startswith('Lcom/example/myapplication'):
        return True
    return False


# Packages found at https://developer.android.com/reference/packages.html
ANDROID_PACAKGES = ["Landroid/", "Lcom/android/internal/util", "Ldalvik/", "Ljava/", "Ljavax/", "Lorg/apache/",
                    "Lorg/json/", "Lorg/w3c/dom/", "Lorg/xml/sax", "Lorg/xmlpull/v1/", "Ljunit/"]

CUSTOM_ANDROID_PACKAGES = ANDROID_PACAKGES + ["Landroidx/", "[Landroidx/"]


def android_class_filter(class_name_prefix: str, _class_analysis: ClassAnalysis):
    for candidate in CUSTOM_ANDROID_PACKAGES:
        if class_name_prefix.startswith(candidate):
            return False
    return True


def diff(old_apk_path, old_apk_session_path, new_apk_path, new_apk_session_path):
    old_apk = AnalyzedApk(old_apk_path, session_path=old_apk_session_path)
    new_apk = AnalyzedApk(new_apk_path, session_path=new_apk_session_path)

    apk_differ = ApkDiffer(old_apk, new_apk)
    apk_differ.filter_classes(android_class_filter)
    apk_differ.pack()
    apk_differ.find_classes_matches()
    pass


def test_apk_info():
    apk = ApkInfo(AnalyzedApk(TOAST_HELLO_APK_PATH, session_path=TOAST_HELLO_SESSION_PATH))
    apk.filter_classes(android_class_filter)
    apk.pack()
    pass


def test_toast_apk():
    diff(TOAST_HELLO_APK_PATH, TOAST_HELLO_SESSION_PATH, TOAST_BYE_APK_PATH, TOAST_BYE_SESSION_PATH)

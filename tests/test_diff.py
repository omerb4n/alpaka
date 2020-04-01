from tests.apks_config.bye_apk_config import TOAST_BYE_APK_PATH, TOAST_BYE_SESSION_PATH
from tests.apks_config.hello_apk_config import TOAST_HELLO_APK_PATH, TOAST_HELLO_SESSION_PATH
from tests.class_filters import android_class_filter
from tests.diff import diff


def test_toast_apk():
    diff(TOAST_HELLO_APK_PATH, TOAST_HELLO_SESSION_PATH, TOAST_BYE_APK_PATH, TOAST_BYE_SESSION_PATH,
         android_class_filter)

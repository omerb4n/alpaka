from tests.apks_config.bye_apk_config import TOAST_BYE_APK_CONFIG
from tests.apks_config.hello_apk_config import TOAST_HELLO_APK_CONFIG
from tests.class_filters import android_class_filter
from tests.diff import diff


def test_toast_apk():
    diff(TOAST_HELLO_APK_CONFIG, TOAST_BYE_APK_CONFIG, android_class_filter)

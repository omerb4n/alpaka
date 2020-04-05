from androguard.core.analysis.analysis import ClassAnalysis

from tests.apks_config.facebook_262_0_0_34_117 import FACEBOOK_262_0_0_34_117_APK_CONFIG
from tests.apks_config.facebook_264_0_0_44_111 import FACEBOOK_264_0_0_44_111_APK_CONFIG
from tests.diff import diff


def filter_facebook_classes(class_name_prefix: str, _class_analysis: ClassAnalysis):
    for package in ['Lcom.facebook.pumpkin/', 'LX/']:
        if class_name_prefix.startswith(package) and not _class_analysis.is_external():
            return True
    return False


def test_facebook_apk():
    diff(FACEBOOK_262_0_0_34_117_APK_CONFIG, FACEBOOK_264_0_0_44_111_APK_CONFIG, filter_facebook_classes)

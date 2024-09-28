from androguard.core.analysis.analysis import ClassAnalysis

from tests.apks_config.whatsapp_2_20_108_apk_config import WHATSAPP_2_20_108_APK_CONFIG
from tests.apks_config.whatsapp_2_20_89_apk_config import WHATSAPP_2_20_89_APK_CONFIG
from tests.diff import diff


def filter_whatsapp_classes(class_name_prefix: str, _class_analysis: ClassAnalysis):
    for package in ['Lcom.whatsapp.location/', 'LX/']:
        if class_name_prefix.startswith(package):
            return True
    return False


def test_whatsapp_apk():
    # TODO: The following line will fail on "Windows fatal exception: stack overflow".
    #  Problem occurs when Androguard will try to pickle dump the session
    # diff(WHATSAPP_2_20_89_APK_CONFIG, WHATSAPP_2_20_108_APK_CONFIG, filter_whatsapp_classes)
    assert False

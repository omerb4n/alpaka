from androguard.core.analysis.analysis import ClassAnalysis

from tests.apks_config.whatsapp_2_20_108_apk_config import WHATSAPP_2_20_108_APK_PATH, WHATSAPP_2_20_108_SESSION_PATH
from tests.apks_config.whatsapp_2_20_89_apk_config import WHATSAPP_2_20_89_APK_PATH, WHATSAPP_2_20_89_SESSION_PATH
from tests.diff import diff


def filter_whatsapp_classes(class_name_prefix: str, _class_analysis: ClassAnalysis):
    for package in ['Lcom.whatsapp.location/', 'LX/']:
        if class_name_prefix.startswith(package):
            return True
    return False


def test_whatsapp_apk():
    diff(WHATSAPP_2_20_89_APK_PATH, WHATSAPP_2_20_89_SESSION_PATH, WHATSAPP_2_20_108_APK_PATH,
         WHATSAPP_2_20_108_SESSION_PATH, filter_whatsapp_classes)

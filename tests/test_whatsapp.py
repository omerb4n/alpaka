import threading

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
    threading.stack_size(50000)
    diff(WHATSAPP_2_20_89_APK_CONFIG.apk_path, WHATSAPP_2_20_89_APK_CONFIG.session_path,
         WHATSAPP_2_20_108_APK_CONFIG.apk_path, WHATSAPP_2_20_108_APK_CONFIG.session_path,
         filter_whatsapp_classes)

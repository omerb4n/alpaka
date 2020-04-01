import os

from tests.apks_config.whatsapp_apks_config import WHATSAPP_APKS_PATH
from tests.conftest import AG_SESSIONS_PATH

APK_NAME = 'com.whatsapp_2.20.108-453352_minAPI15(armeabi-v7a)(nodpi)_apkmirror.com.apk'

WHATSAPP_2_20_108_APK_PATH = os.path.join(WHATSAPP_APKS_PATH, f'{APK_NAME}.apk')
WHATSAPP_2_20_108_SESSION_PATH = os.path.join(AG_SESSIONS_PATH, f'{APK_NAME}.ag')

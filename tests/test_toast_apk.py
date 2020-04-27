import json

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk_differ import ApkDiffer
from alpaka.encoders.classes_matches_encoder import convert_class_matches_dict_to_output_format
from alpaka.obfuscation_detection.score_based_detection import  ScoreBasedObfuscationDetector
from tests.apks_config.bye_apk_config import TOAST_BYE_APK_CONFIG
from tests.apks_config.hello_apk_config import TOAST_HELLO_APK_CONFIG
from tests.class_filters import android_class_filter


def test_toast_apk():
    old_apk = AnalyzedApk(TOAST_HELLO_APK_CONFIG.apk_path,
                          session_path=TOAST_HELLO_APK_CONFIG.session_path)
    new_apk = AnalyzedApk(TOAST_BYE_APK_CONFIG.apk_path,
                          session_path=TOAST_BYE_APK_CONFIG.session_path)

    apk_differ = ApkDiffer(ScoreBasedObfuscationDetector(), [android_class_filter])
    matches = apk_differ.diff(old_apk, new_apk)
    matches_output = convert_class_matches_dict_to_output_format(matches)
    print(json.dumps(matches_output, indent=4))

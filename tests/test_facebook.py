import json

from androguard.core.analysis.analysis import ClassAnalysis

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk.package_info import PackageInfo
from alpaka.apk_differ import ApkDiffer
from alpaka.encoders.classes_matches_encoder import convert_class_matches_dict_to_output_format
from alpaka.obfuscation_detection.score_based_detection import ObfuscationDetector
from tests.apks_config.facebook_262_0_0_34_117 import FACEBOOK_262_0_0_34_117_APK_CONFIG
from tests.apks_config.facebook_264_0_0_44_111 import FACEBOOK_264_0_0_44_111_APK_CONFIG
from tests.class_filters import android_class_filter


def filter_facebook_classes(class_name_prefix: str, _class_analysis: ClassAnalysis):
    for package in ['Lcom/facebook/pumpkin/', 'LX/']:
        if class_name_prefix.startswith(package) and not _class_analysis.is_external():
            return True
    return False


class FacebookClassNameOD(ObfuscationDetector):
    def is_obfuscated(self, class_name_prefix: str) -> bool:
        package_name = PackageInfo.get_package_name(PackageInfo.get_parent_package_name_prefix(class_name_prefix))
        if package_name == 'X':
            return True
        else:
            return False


class FacebookPackageNameOD(ObfuscationDetector):
    def is_obfuscated(self, package_name_prefix: str) -> bool:
        if PackageInfo.get_package_name(package_name_prefix) == 'X':
            return True
        else:
            return False


def test_facebook_apk():
    old_apk = AnalyzedApk(FACEBOOK_262_0_0_34_117_APK_CONFIG.apk_path,
                          session_path=FACEBOOK_262_0_0_34_117_APK_CONFIG.session_path)
    new_apk = AnalyzedApk(FACEBOOK_264_0_0_44_111_APK_CONFIG.apk_path,
                          session_path=FACEBOOK_264_0_0_44_111_APK_CONFIG.session_path)

    apk_differ = ApkDiffer(FacebookPackageNameOD(), FacebookClassNameOD(), [android_class_filter()])
    matches = apk_differ.diff(old_apk, new_apk)
    matches_output = convert_class_matches_dict_to_output_format(matches)
    print(json.dumps(matches_output, indent=4))

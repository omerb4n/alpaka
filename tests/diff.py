import json
from typing import Callable

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk_differ import ApkDiffer
from alpaka.encoders.classes_matches_encoder import convert_class_matches_dict_to_output_format
from alpaka.obfuscation_detection.score_based_detection import ScoreBasedObfuscationDetector
from tests.apks_config.apk_config import ApkConfig


def diff(old_apk_config: ApkConfig, new_apk_config: ApkConfig, class_filter: Callable = None):
    old_apk = AnalyzedApk(old_apk_config.apk_path, session_path=old_apk_config.session_path)
    new_apk = AnalyzedApk(new_apk_config.apk_path, session_path=new_apk_config.session_path)

    filters = []
    if class_filter is not None:
        filters.append(class_filter)

    apk_differ = ApkDiffer(ScoreBasedObfuscationDetector(), filters)
    matches = apk_differ.diff(old_apk, new_apk)
    matches_output = convert_class_matches_dict_to_output_format(matches)
    print(json.dumps(matches_output, indent=4))

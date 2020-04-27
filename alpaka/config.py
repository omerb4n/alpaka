import json
import os.path


def _load_signature_distance_weights():
    weights_file_path = os.path.join(_get_config_dir_path(), 'weights.json')
    with open(weights_file_path, 'r') as weights_file:
        return json.load(weights_file)


def _get_config_dir_path():
    this_script_path = os.path.realpath(__file__)
    alpaka_package_path = os.path.dirname(this_script_path)
    return os.path.join(alpaka_package_path, 'config')


OUTPUT_PATH = "output"
MAXIMUM_SIGNATURE_MATCHES = 3
DEFAULT_WEIGHTS = _load_signature_distance_weights()

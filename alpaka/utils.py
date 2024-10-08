import os
import shutil
import subprocess
from typing import List, Dict

from alpaka.colors import bcolors
from alpaka.constants import PACKAGE_NAME_SEPARATOR


def validate_file_exists(path):
    if not os.path.isfile(path):
        raise OSError(f'Given path {path} is not an existing file')


def validate_directory_exists(path):
    if not os.path.isdir(path):
        raise OSError(f'Given path {path} is not an existing directory')


def clean_dir(path):
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)


def _apktool_decode(apk_path, output_path):
    print(f"Running apktool against '{bcolors.OKBLUE}{apk_path}{bcolors.ENDC}' into '{output_path}'")
    subprocess.call(["apktool", "d", "--no-debug-info", "-f", "-o", output_path, apk_path], shell=True)
    print(f"[{bcolors.OKGREEN}OK{bcolors.ENDC}]")


def extract_apk(apk_path, output_path):
    # Make sure the paths exist
    validate_file_exists(apk_path)
    validate_directory_exists(output_path)

    _apktool_decode(apk_path, output_path)


class DictFilterMixin(Dict):

    """
    A mixin for a dict subclass implementing filtering in-place
    """

    def filter(self, filter_function):
        for key, value in list(self.items()):
            if not filter_function(key, value):
                del self[key]


def calc_average(l: List):
    return sum(l) / len(l)


def split_by_separators(text: str, seperators: List[str]):
    previous_word_index = 0
    words = []
    for i in range(1, len(text)):
        if text[i] in seperators:
            words.append(text[previous_word_index:i])
            previous_word_index = i
    words.append(text[previous_word_index:len(text)])
    return words


def get_domain_name(domain):
    return domain[domain.rfind(PACKAGE_NAME_SEPARATOR) + 1:]


def get_subdomain(domain):
    return domain[:domain.rfind(PACKAGE_NAME_SEPARATOR)]

import os
import shutil
import subprocess

from alpaka.colors import bcolors


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


def filter_dict(dictionary: dict, filter_function):
    return {k: v for k, v in dictionary.items() if filter_function(k, v)}

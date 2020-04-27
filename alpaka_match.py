import json
import importlib.machinery
import importlib.util
from argparse import ArgumentParser

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk_differ import ApkDiffer
from alpaka.encoders.classes_matches_encoder import convert_class_matches_dict_to_output_format
from alpaka.obfuscation_detection.simple_detection import SimpleObfuscationDetector


class ExternalComponentLoadError(RuntimeError):
    """
    Raised when loading a component from an external module failed
    """


def main():
    args = parse_arguments()
    apk1 = AnalyzedApk(args.apk_1)
    apk2 = AnalyzedApk(args.apk_2)

    apk_differ = create_apk_differ(apk1, apk2, args.filter, args.obfuscation_detector)

    class_matches = apk_differ.diff(
        apk1,
        apk2,
        match_packages=args.match_packages,
        match_by_name=args.match_by_name,
    )
    output_matches(args.result_file_path, class_matches)


def create_apk_differ(apk1, apk2, filter_module_path, obfuscation_detector_module_path):
    filter_funcs = []
    if filter_module_path is not None:
        filter_funcs = [load_filter(filter_module_path)]
    obfuscation_detector_type = SimpleObfuscationDetector
    if obfuscation_detector_module_path is not None:
        obfuscation_detector_type = load_obfuscation_detector_type(obfuscation_detector_module_path)
    apk_differ = ApkDiffer(obfuscation_detector_type(apk1.analysis, apk2.analysis), filter_funcs)
    return apk_differ


def output_matches(result_file_path, class_matches):
    output = convert_class_matches_dict_to_output_format(class_matches)
    with open(result_file_path, 'w') as result_file:
        json.dump(output, result_file, indent=4)


def parse_arguments():
    parser = ArgumentParser(description='Find class matches between 2 apk versions')
    parser.add_argument('apk_1')
    parser.add_argument('apk_2')
    parser.add_argument('result_file_path')
    parser.add_argument('-p', '--no-package-matching', dest='match_packages', action='store_false',
                        help='Disables matching the packages before matching the classes.'
                             ' Not recommended for large apk files.')
    parser.add_argument('-n', '--no-name-matching', dest='match_by_name', action='store_false',
                        help='Disables matching the unobfuscated classes by name.')
    parser.add_argument('-f', '--filter', '--class-filter', dest='filter',
                        help='An external module containing a class filter. Read full docs for more info.')
    parser.add_argument('-o', '--obfuscation-detector', dest='obfuscation_detector',
                        help='An external module containing an obfuscation detector. Read full docs for more info.')
    return parser.parse_args()


def load_filter(filter_module_path):
    try:
        filter_module = import_external_module('external_class_filter', filter_module_path)
        return filter_module.external_filter
    except (ImportError, AttributeError) as e:
        raise ExternalComponentLoadError('Failed loading the external class filter') from e


def load_obfuscation_detector_type(obfuscaion_detector_module_path):
    try:
        obfuscation_detector_module = import_external_module(
            'external_obfuscation_detector',
            obfuscaion_detector_module_path
        )
        return obfuscation_detector_module.ExternalObfuscationDetector
    except (ImportError, AttributeError) as e:
        raise ExternalComponentLoadError('Failed loading the external obfuscation detector') from e


def import_external_module(module_name, module_path):
    loader = importlib.machinery.SourceFileLoader(module_name, module_path)
    spec = importlib.util.spec_from_loader(loader.name, loader)
    module = importlib.util.module_from_spec(spec)
    loader.exec_module(module)
    return module


if __name__ == '__main__':
    main()

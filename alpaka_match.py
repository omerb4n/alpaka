import json
from argparse import ArgumentParser

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk_differ import ApkDiffer
from alpaka.encoders.classes_matches_encoder import convert_class_matches_dict_to_output_format
from alpaka.obfuscation_detection.simple_detection import SimpleObfuscationDetector


def main():
    apk1_path, apk2_path, result_file_path, match_packages = parse_arguments()
    apk1 = AnalyzedApk(apk1_path)
    apk2 = AnalyzedApk(apk2_path)
    apk_differ = ApkDiffer(SimpleObfuscationDetector(apk1.analysis, apk2.analysis))
    class_matches = apk_differ.diff(apk1, apk2)
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
    args = parser.parse_args()
    return args.apk_1, args.apk_2, args.result_file_path, args.match_packages


if __name__ == '__main__':
    main()

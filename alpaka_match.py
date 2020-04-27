import json
from argparse import ArgumentParser

from alpaka.apk.analyzed_apk import AnalyzedApk
from alpaka.apk_differ import ApkDiffer
from alpaka.encoders.classes_matches_encoder import convert_class_matches_dict_to_output_format
from alpaka.obfuscation_detection.simple_detection import SimpleObfuscationDetector


def main():
    args = parse_arguments()
    apk1 = AnalyzedApk(args.apk1_path)
    apk2 = AnalyzedApk(args.apk2_path)
    apk_differ = ApkDiffer(SimpleObfuscationDetector(apk1.analysis, apk2.analysis))
    class_matches = apk_differ.diff(
        apk1,
        apk2,
        match_packages=args.match_packages,
        match_by_name=args.match_by_name,
    )
    output = convert_class_matches_dict_to_output_format(class_matches)
    with open(args.result_file_path, 'w') as result_file:
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
    return parser.parse_args()


if __name__ == '__main__':
    main()

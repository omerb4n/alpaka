import difflib
import json
import os
from argparse import ArgumentParser
from enum import Enum

from prompt_toolkit.lexers import PygmentsLexer
from pygments.lexers.diff import DiffLexer
from pypager.pager import Pager
from pypager.source import StringSource


class Mode(Enum):
    SMALI = 'smali'
    JAVA = 'java'

    def __str__(self):
        return self.value


def main():
    matches_file_path, apk1_dir, apk2_dir, mode = parse_arguments()
    with open(matches_file_path, 'r') as matches_file:
        matches = json.load(matches_file)
    diff_finder = AlpakaDiffFinder(apk1_dir, apk2_dir, mode, matches)

    print_help_message(apk1_dir, apk2_dir)
    while True:
        user_input = input()
        if user_input in ('quit', 'exit', 'q'):
            return
        if user_input == 'help':
            print_help_message(apk1_dir, apk2_dir)
            continue
        if user_input == '':
            continue

        try:
            diff_pager = diff_finder.get_match_diff(user_input)
        except IOError as e:
            print(f'Cannot read the code for one of the classes: {e}')
            continue
        if diff_pager is None:
            print(f'No match found for class {user_input}')
            continue
        diff_pager.run()


def print_help_message(apk1_dir, apk2_dir):
    print(
        'Alpaka diff terminal\n'
        f'Comparing {apk1_dir} and {apk2_dir}\n'
        '\n'
        'Special Commands:\n'
        '- help: print this help message\n'
        '- exit/quit/q: close the program\n'
        '\n'
        'To compare a class from apk 1 to the matching class from apk 2, type the full class identifier\n'
        '(com.foo.Bar for java mode, Lcom/foo/Bar; for smali mode)\n'
    )


def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument('matches_file', help='The JSON file containing the class matches, generated by alpaka_match.py')
    parser.add_argument('apk1_source_dir', help='The sources directory (java or smali) of the first apk version.')
    parser.add_argument('apk2_source_dir', help='The sources directory (java or smali) of the second apk version.')
    parser.add_argument('mode', type=Mode, choices=list(Mode), help='The compared source type. Either java or smali.')
    args = parser.parse_args()
    return args.matches_file, args.apk1_source_dir, args.apk2_source_dir, args.mode


class AlpakaDiffFinder:

    def __init__(self, sources1_path, sources2_path, mode, matches):
        self._apk1_class_finder = ClassFileFinder(mode, sources1_path)
        self._apk2_class_finder = ClassFileFinder(mode, sources2_path)
        self._mode = mode
        self._matches = matches

    def get_match_diff(self, class_identifier):
        match_identifier = self.get_matching_class(class_identifier)
        if match_identifier is None:
            return None
        class_code = self._apk1_class_finder.get_class_code(class_identifier)
        match_code = self._apk2_class_finder.get_class_code(match_identifier)
        return self._create_diff_pager(class_identifier, class_code, match_identifier, match_code)

    def get_matching_class(self, class_identifier):
        if self._mode is Mode.JAVA:
            class_identifier = self.java_class_identifier_to_smali(class_identifier)
        try:
            class_matches = self._matches[class_identifier].items()
            best_match = min(class_matches, key=lambda x: x[1])[0]
            if self._mode is Mode.JAVA:
                best_match = self.smali_class_identifier_to_java(best_match)
            return best_match
        except (KeyError, IndexError, ValueError):
            return None

    @classmethod
    def java_class_identifier_to_smali(cls, java_class_name):
        slash_separated = java_class_name.replace('.', '/')
        return f'L{slash_separated};'

    @classmethod
    def smali_class_identifier_to_java(cls, smali_class_name):
        return smali_class_name[1:-1].replace('/', '.')

    @classmethod
    def _create_diff_pager(cls, class_name, class_code, match_name, match_code):
        diff = ''.join(difflib.unified_diff(
            class_code.splitlines(keepends=True),
            match_code.splitlines(keepends=True),
            fromfile=f'apk 1: {class_name}',
            tofile=f'apk 2: {match_name}',
        ))
        if diff == '':
            diff = f'No diff between apk 1: {class_name} and apk 2: {match_name}'
        pager = Pager()
        pager_source = StringSource(diff, lexer=PygmentsLexer(DiffLexer))
        pager.add_source(pager_source)
        return pager


class ClassFileFinder:

    def __init__(self, mode, sources_dir_path):
        self._mode = mode
        self._sources_dir_path = sources_dir_path

    def get_class_code(self, class_identifier):
        file_path = self.get_file_path_for_class(class_identifier)
        with open(os.path.join(self._sources_dir_path, file_path), 'r') as class_file:
            return class_file.read()

    def get_file_path_for_class(self, class_identifier):
        class_file_path = os.path.join(*self._split_class_identifier(class_identifier))
        if self._mode is Mode.JAVA:
            class_file_path += '.java'
        elif self._mode is Mode.SMALI:
            class_file_path = self._find_smali_file_by_extensionless_path(class_file_path)
        return class_file_path

    def _find_smali_file_by_extensionless_path(self, incomplete_class_file_path):
        """
        Smali file names sometimes have numbered extensions on them if
        the filesystem doesn't support case sensitivity.
        Therefore, instead of appending '.smali', we have to search in the relevant directory for a match.
        :param incomplete_class_file_path: a file path to the smali file, without the .<number>.smali extension
        :return: the complete file path
        """
        class_dir, filename_start = os.path.split(incomplete_class_file_path)
        filename_start += '.'
        for possible_filename in os.listdir(os.path.join(self._sources_dir_path, class_dir)):
            if possible_filename.startswith(filename_start):
                return os.path.join(class_dir, possible_filename)
        raise IOError('Matching smali file not found')

    def _split_class_identifier(self, class_identifier):
        if self._mode is Mode.SMALI:
            return class_identifier[1:-1].split('/')
        return class_identifier.split('.')


if __name__ == '__main__':
    main()

import re
import string
from typing import Sized, Sequence, List

import enchant

from alpaka.exceptions import FormatError
from alpaka.obfuscation.types import ScoreSystem, ScoreWeight, GradeSystem, ObfuscationDetector
from alpaka.utils import calc_average, split_by_separators


class GrowthScoreSystem(ScoreSystem):
    def __init__(self, best_value, worst_value, score_growth):
        super(GrowthScoreSystem, self).__init__()
        self._best_value = best_value
        self._worst_value = worst_value
        self.score_growth = score_growth

    def _calc_score(self, value):
        if value >= self._best_value:
            return self.MAXIMUM_SCORE
        elif value <= self._worst_value:
            return self.MINIMUM_SCORE
        else:
            return value * (self.score_growth * value)


class IsWordEnglishScore(ScoreSystem):
    def _calc_score(self, word):
        english_dict = enchant.Dict("en_US")
        if english_dict.check(word):
            return self.MAXIMUM_SCORE
        else:
            return self.MINIMUM_SCORE


class LengthScore(GrowthScoreSystem):
    def _calc_score(self, sized: Sized):
        return super(LengthScore, self)._calc_score(len(sized))


class CharactersScore(ScoreSystem):
    def __init__(self, allowed_characters: List[str]):
        self._allowed_characters = allowed_characters
        super(CharactersScore, self).__init__()

    def _calc_score(self, word):
        if all([char in self._allowed_characters for char in word]):
            return self.MAXIMUM_SCORE
        else:
            return self.MINIMUM_SCORE


class AverageScore(ScoreSystem):
    def __init__(self, score_system: ScoreSystem):
        self._score_system = score_system

    def _calc_score(self, obj_sequence: Sequence):
        obj_scores = [self._score_system.calc_score(obj) for obj in obj_sequence]
        return calc_average(obj_scores)


class UpperCamelCaseGrade(GradeSystem):
    def _calc_score(self, upper_camel_case_text: str):
        # Remove $ for Class name grade
        upper_camel_case_text.replace('$', '')
        if upper_camel_case_text[0] not in string.ascii_uppercase:
            raise FormatError(f"'{upper_camel_case_text}' does not meet the UpperCamelCase convention")
        upper_camel_case_words = split_by_separators(upper_camel_case_text, string.ascii_uppercase)
        return super(UpperCamelCaseGrade, self)._calc_score(upper_camel_case_words)


class UnderscoreNameGrade(GradeSystem):
    def _calc_score(self, underscore_name):
        underscore_split = underscore_name.split('_')
        return super(UnderscoreNameGrade, self)._calc_score(underscore_split)


class PackageNameObfuscationDetector(ObfuscationDetector):
    # Word length score
    WORD_BEST_LENGTH = 8
    WORD_WORST_LENGTH = 2
    WORD_LENGTH_SCORE_GROWTH = ScoreSystem.MAXIMUM_SCORE / WORD_BEST_LENGTH ** 2

    # Word grade score weights
    WORD_LENGTH_WEIGHT = 0.4
    IS_WORD_ENGLISH_WEIGHT = 0.6

    WORD_AVERAGE_WEIGHT = 0.9

    # Words count score
    BEST_WORDS_COUNT = 4
    WORST_WORDS_COUNT = 1
    WORDS_COUNT_GROWTH = ScoreSystem.MAXIMUM_SCORE / BEST_WORDS_COUNT ** 2

    WORDS_COUNT_WEIGHT = 0.1

    # Underscore score
    UNDERSCORE_WEIGHT = 0.8

    # Characters score
    CHARACTERS_WEIGHT = 0.2

    PASS_SCORE = 0.6

    def __init__(self):
        length_score_weight = ScoreWeight(
            LengthScore(self.WORD_BEST_LENGTH, self.WORD_WORST_LENGTH, self.WORD_LENGTH_SCORE_GROWTH),
            self.WORD_LENGTH_WEIGHT)
        is_word_english_score_weight = ScoreWeight(IsWordEnglishScore(), self.IS_WORD_ENGLISH_WEIGHT)
        average_score_score_weight = ScoreWeight(AverageScore(
            GradeSystem([length_score_weight, is_word_english_score_weight])),
            self.WORD_AVERAGE_WEIGHT)
        word_count_score_weight = ScoreWeight(
            LengthScore(self.BEST_WORDS_COUNT, self.WORST_WORDS_COUNT, self.WORDS_COUNT_GROWTH),
            self.WORDS_COUNT_WEIGHT)
        characters_score_weight = ScoreWeight(CharactersScore(list(string.ascii_letters) + ['_']), self.CHARACTERS_WEIGHT)

        underscore_score_weight = ScoreWeight(
            UnderscoreNameGrade([average_score_score_weight, word_count_score_weight]),
            self.UNDERSCORE_WEIGHT)
        self.grade_system = GradeSystem([underscore_score_weight, characters_score_weight],
                                        self.PASS_SCORE)

    def is_obfuscated(self, package_name: str):
        return not self.grade_system.did_pass(package_name)


class ClassNameObfuscationDetector(ObfuscationDetector):
    KNOWN_OBFUSCATED_PATTERNS = ["^AnonymousClass[\d\w]*$"]
    # Word length score
    WORD_BEST_LENGTH = 8
    WORD_WORST_LENGTH = 2
    WORD_LENGTH_SCORE_GROWTH = ScoreSystem.MAXIMUM_SCORE / WORD_BEST_LENGTH ** 2

    # Word grade score weights
    WORD_LENGTH_WEIGHT = 0.6
    IS_WORD_ENGLISH_WEIGHT = 0.4

    WORD_AVERAGE_WEIGHT = 0.9

    # Words count score
    BEST_WORDS_COUNT = 3
    WORST_WORDS_COUNT = 1
    WORDS_COUNT_GROWTH = ScoreSystem.MAXIMUM_SCORE / BEST_WORDS_COUNT ** 2

    WORDS_COUNT_WEIGHT = 0.1

    # UpperCamelCase score
    UPPER_CAMEL_CASE_WEIGHT = 0.9

    # Characters score
    CHARACTERS_WEIGHT = 0.1

    PASS_SCORE = 0.6

    def __init__(self):
        length_score_weight = ScoreWeight(
            LengthScore(self.WORD_BEST_LENGTH, self.WORD_WORST_LENGTH, self.WORD_LENGTH_SCORE_GROWTH),
            self.WORD_LENGTH_WEIGHT)
        is_word_english_score_weight = ScoreWeight(IsWordEnglishScore(), self.IS_WORD_ENGLISH_WEIGHT)
        average_score_score_weight = ScoreWeight(AverageScore(
            GradeSystem([length_score_weight, is_word_english_score_weight])),
            self.WORD_AVERAGE_WEIGHT)
        word_count_score_weight = ScoreWeight(
            LengthScore(self.BEST_WORDS_COUNT, self.WORST_WORDS_COUNT, self.WORDS_COUNT_GROWTH),
            self.WORDS_COUNT_WEIGHT)
        characters_score_weight = ScoreWeight(CharactersScore(list(string.ascii_letters) + ['$']), self.CHARACTERS_WEIGHT)

        upper_camel_case_score_weight = ScoreWeight(
            UpperCamelCaseGrade([average_score_score_weight, word_count_score_weight]), self.UPPER_CAMEL_CASE_WEIGHT)
        self.class_name_grade = GradeSystem([upper_camel_case_score_weight, characters_score_weight], self.PASS_SCORE)

    def is_obfuscated(self, class_name: str):
        if self.is_known_obfuscated_pattern(class_name):
            return True
        else:
            try:
                return not self.class_name_grade.did_pass(class_name)
            except FormatError:
                return WordObfuscationDetector().is_obfuscated(class_name)

    def is_known_obfuscated_pattern(self, class_name: str) -> bool:
        for regex in self.KNOWN_OBFUSCATED_PATTERNS:
            if re.search(regex, class_name):
                return True
        return False


class WordObfuscationDetector(ObfuscationDetector):
    # LengthScoreWeight
    BEST_LENGTH = 10
    WORST_LENGTH = 4
    LENGTH_SCORE_GROWTH = ScoreSystem.MAXIMUM_SCORE / BEST_LENGTH ** 2

    # Score Weights
    LENGTH_SCORE_WEIGHT = 0.4
    IS_WORD_ENGLISH_SCORE_WEIGHT = 0.3
    WORD_CHARACTERS_SCORE_WEIGHT = 0.3

    PASS_GRADE = 0.5

    def __init__(self):
        length_score_weight = ScoreWeight(
            LengthScore(self.BEST_LENGTH, self.WORST_LENGTH, self.LENGTH_SCORE_GROWTH), self.LENGTH_SCORE_WEIGHT)
        is_word_english_score_weight = ScoreWeight(IsWordEnglishScore(), self.IS_WORD_ENGLISH_SCORE_WEIGHT)
        word_characters_score_weight = ScoreWeight(CharactersScore(list(string.ascii_letters)), self.WORD_CHARACTERS_SCORE_WEIGHT)
        self.word_grade_system = GradeSystem(
            [length_score_weight, is_word_english_score_weight, word_characters_score_weight], self.PASS_GRADE)

    def is_obfuscated(self, word: str):
        return not self.word_grade_system.did_pass(word)

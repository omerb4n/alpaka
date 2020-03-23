import abc
import string
from typing import List, Sized

import enchant

from alpaka.exceptions import FormatError
from alpaka.utils import calc_average, split_by_uppercase


class ScoreSystem(abc.ABC):
    MAXIMUM_SCORE = 1.0
    MINIMUM_SCORE = 0.0

    def __init__(self, pass_score=MINIMUM_SCORE):
        self._pass_score = pass_score

    @abc.abstractmethod
    def _calc_score(self, obj):
        raise NotImplementedError()

    def calc_score(self, obj):
        return max(self.MINIMUM_SCORE, min(self.MAXIMUM_SCORE, self._calc_score(obj)))

    def did_pass(self, obj):
        return not (self.calc_score(obj) >= self._pass_score)


class ObfuscationDetector(abc.ABC):
    def __init__(self, score_system: ScoreSystem):
        self.score_system = score_system

    def is_obfuscated(self, obj):
        return self.score_system.did_pass(obj)


class GrowthScoreSystem(ScoreSystem):
    def __init__(self, best_value, worst_value, score_growth, *args, **kwargs):
        super(GrowthScoreSystem, self).__init__(*args, **kwargs)
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


class WordCharactersScore(ScoreSystem):
    def _calc_score(self, word):
        if all([char in string.ascii_letters for char in word]):
            return self.MAXIMUM_SCORE
        else:
            return self.MINIMUM_SCORE


class WordScore(ScoreSystem):
    IS_ENGLISH_WEIGHT = 0.3 * ScoreSystem.MAXIMUM_SCORE
    LENGTH_WEIGHT = 0.4 * ScoreSystem.MAXIMUM_SCORE
    CHARACTERS_WEIGHT = 0.3 * ScoreSystem.MAXIMUM_SCORE

    BEST_LENGTH = 15
    WORST_LENGTH = 4
    LENGTH_SCORE_GROWTH = ScoreSystem.MAXIMUM_SCORE / BEST_LENGTH ** 2

    DEFAULT_PASS_SCORE = 0.5

    def __init__(self, pass_score=DEFAULT_PASS_SCORE):
        super(WordScore, self).__init__(pass_score)

    def _calc_score(self, word):
        score = self.MINIMUM_SCORE
        score += LengthScore(self.BEST_LENGTH, self.WORST_LENGTH, self.LENGTH_SCORE_GROWTH).calc_score(
            word) * self.LENGTH_WEIGHT
        score += IsWordEnglishScore().calc_score(word) * self.IS_ENGLISH_WEIGHT
        score += WordCharactersScore().calc_score(word) * self.CHARACTERS_WEIGHT
        return score


class WordObfuscationDetector(ObfuscationDetector):
    def __init__(self):
        super(WordObfuscationDetector, self).__init__(WordScore())


class WordsAverageScore(ScoreSystem):
    def _calc_score(self, words: List):
        words_score = [WordScore().calc_score(word) for word in words]
        return calc_average(words_score)


class UpperCamelCaseScore(ScoreSystem):
    BEST_WORDS_COUNT = 3
    WORST_WORDS_COUNT = 1
    WORDS_COUNT_GROWTH = ScoreSystem.MAXIMUM_SCORE / BEST_WORDS_COUNT ** 2

    WORDS_AVERAGE_SCORE_WEIGHT = 0.8
    WORDS_COUNT_SCORE_WEIGHT = 0.2

    DEFAULT_PASS_SCORE = 0.4

    def __init__(self, pass_score=DEFAULT_PASS_SCORE):
        super(UpperCamelCaseScore, self).__init__(pass_score)

    def _calc_score(self, upper_camel_case_text):
        score = self.MINIMUM_SCORE
        if upper_camel_case_text[0] not in string.ascii_uppercase:
            raise FormatError(f"'{upper_camel_case_text}' does not meet the UpperCamelCase convention")
        upper_camel_case_words = split_by_uppercase(upper_camel_case_text)
        score += WordsAverageScore().calc_score(upper_camel_case_words) * self.WORDS_AVERAGE_SCORE_WEIGHT
        words_count_score_system = LengthScore(self.BEST_WORDS_COUNT, self.WORST_WORDS_COUNT, self.WORDS_COUNT_GROWTH)
        score += words_count_score_system.calc_score(upper_camel_case_words) * self.WORDS_COUNT_SCORE_WEIGHT
        return score


class ClassNameObfuscationDetector(ObfuscationDetector):
    def __init__(self):
        super(ClassNameObfuscationDetector, self).__init__(UpperCamelCaseScore())

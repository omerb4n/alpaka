import re
import string

import enchant

MAXIMUM_WORD_SCORE = 1
MINIMUM_WORD_SCORE = 0
PASS_SCORE = 0.5

IS_ENGLISH_WEIGHT = 0.2 * MAXIMUM_WORD_SCORE
LENGTH_WEIGHT = 0.5 * MAXIMUM_WORD_SCORE
CHARACTERS_WEIGHT = 0.3 * MAXIMUM_WORD_SCORE

GREAT_LENGTH = 15
BAD_LENGTH = 4
LENGTH_GROWTH = 1 / GREAT_LENGTH ** 2


def split_by_uppercase(concatenated_words):
    return re.findall('[A-Z][^A-Z]*', concatenated_words)


def is_obfuscated_class_name(name: str):
    """
    In Java and Kotlin, class names are written in UpperCamelCase convention.
    :param name:
    :return:
    """
    if name[0] in string.ascii_uppercase:
        upper_camel_case_words = split_by_uppercase(name)
        if len(upper_camel_case_words) > 1:
            words_score = [calc_word_score(word) for word in upper_camel_case_words]
            return sum(words_score) / len(words_score)
    return is_obfuscated_word(name)


def calc_word_is_english(word):
    english_dict = enchant.Dict("en_US")
    if english_dict.check(word):
        return MAXIMUM_WORD_SCORE
    else:
        return MINIMUM_WORD_SCORE


def calc_word_characters_score(word):
    if all([char in string.ascii_letters for char in word]):
        return MAXIMUM_WORD_SCORE
    else:
        return MINIMUM_WORD_SCORE


def calc_word_length_score(word):
    length = len(word)
    if length >= GREAT_LENGTH:
        return MAXIMUM_WORD_SCORE
    elif length <= BAD_LENGTH:
        return MINIMUM_WORD_SCORE
    else:
        result = length * (LENGTH_GROWTH * length)
        return result if result <= MAXIMUM_WORD_SCORE else MAXIMUM_WORD_SCORE


def calc_word_score(word):
    score = MINIMUM_WORD_SCORE
    score += calc_word_is_english(word) * IS_ENGLISH_WEIGHT
    score += calc_word_length_score(word) * LENGTH_WEIGHT
    score += calc_word_characters_score(word) * CHARACTERS_WEIGHT
    return score


def is_obfuscated_word(word):
    return calc_word_score(word) < PASS_SCORE

# -*- coding: utf-8 -*-
"""
Created Jan 2020

@author: ijovin

Common date conversion and date manipulation functions.

"""
import inflect
from datetime import datetime
from dateutil.parser import parse


def convert_date(date):
    date_normalized = _ordinal_sentence2num(date)
    try:
        if not _check_date_missing_elements(date_normalized):
            return None
        date_parsed = parse(date_normalized, fuzzy=True)
        date_converted = date_parsed.date()
        return str(date_converted)
    except ValueError:
        return None


def _ordinal_sentence2num(sentence):
    word_to_number_mapping = {}
    p = inflect.engine()
    for i in range(1, 32):
        word_form = p.number_to_words(i)
        ordinal_word = p.ordinal(word_form)
        ordinal_number = p.ordinal(i)
        word_to_number_mapping[ordinal_word] = ordinal_number

    sentence_normalized_words = []
    for word in sentence.split():
        word_lower = word.lower()
        if word_lower in word_to_number_mapping:
            sentence_normalized_words.append(word_to_number_mapping[word_lower])
        else:
            sentence_normalized_words.append(word)

    sentence_normalized = ' '.join(sentence_normalized_words)

    return sentence_normalized


def _check_date_missing_elements(date):
    dflt_1 = datetime(1, 1, 1)
    dflt_2 = datetime(2, 2, 2)
    try:
        date_check_1 = parse(date, fuzzy=True, default=dflt_1)
        date_check_2 = parse(date, fuzzy=True, default=dflt_2)
        check_day = date_check_1.day != date_check_2.day
        check_month = date_check_1.month != date_check_2.month
        check_year = date_check_1.year != date_check_2.year

        if check_day or check_month or check_year:
            return False
    except Exception as e:
        return False
    return True
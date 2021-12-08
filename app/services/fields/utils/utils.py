from app.constants import duration_word_inclusions, date_word_exclusions, money_word_exclusions, written_numbers
from .date_utils import convert_date


def is_valid_token(spacy_tkn):
    return not spacy_tkn.is_stop and not spacy_tkn.is_punct and len(spacy_tkn.text) > 1 and \
           spacy_tkn.text.strip() not in [')', '(', '\n', ''] and \
           spacy_tkn.pos_ not in ['CONJ', 'CCONJ', 'NUM', 'PRON', 'PROPN', 'SYM']


def is_duration(entity_text, entity_pos):
    is_duration_included = any(duration_word in entity_text.lower() for duration_word in duration_word_inclusions)
    is_number_included = any(written_number in entity_text.lower() for written_number in written_numbers)
    return is_number_included and is_duration_included


def is_date(entity_text, entity_pos):
    converted_date = convert_date(entity_text.lower())
    is_date_excluded = any(date_word == token for date_word in date_word_exclusions for token in entity_text.lower().split())
    return converted_date is not None and not is_date_excluded


def is_money(entity_text, entity_pos):
    is_money_excluded = any(money_word == token for money_word in money_word_exclusions for token in entity_text.lower().split())
    return (entity_pos == 'NUM' or entity_pos == 'SYM') and not is_money_excluded

# -*- coding: utf-8 -*-
duration_word_inclusions = set(['day', 'week', 'month', 'year'])
written_numbers = set(['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven',
                     'twelve', 'thirteen', 'fourteen', 'fifteen', 'sixteen', 'seventeen', 'eighteen', 'nineteen', 'twenty',
                     'thirty', 'forty', 'fifty', 'sixty', 'seventy', 'eighty', 'ninety', 'hundred', 'thousand', 'million',
                     '1','2','3', '4','5','6','7','8','9','0'])

money_word_exclusions = set(['client'])

date_word_exclusions = set(['present', 'now', 'time', 'currently', 'previously', 'past'])

HIGH_CONFIDENCE_THRESHOLD = 0.8
MEDIUM_CONFIDENCE_THRESHOLD = 0.6

HIGH_CONFIDENCE = 'high'
MEDIUM_CONFIDENCE = 'medium'
LOW_CONFIDENCE = 'low'

SPACY_MODEL = 'en_core_web_lg'

ERROR_BLOB_DOESNT_EXIST = "Specified blob doesn't exist."

TOPN = 5 # number of words to take to the left and right of a field

CLAUSE_ENCODER = 'models/legal_bert_small_smoothing-0.1'

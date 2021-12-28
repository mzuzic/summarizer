from app.model_repository import nlp


def tokenize_sentence(nlp_sentence):
    """
        Returns a spaCy-tokenized sentence (ability to use all spaCy functions and methods)
        :param sentence: the sentence being tokenized (string)
    """
    spans = _get_spans(nlp_sentence)
    spans = _filter_spans(spans)

    with nlp_sentence.retokenize() as retokenizer:
        for span in spans:
            retokenizer.merge(span)

    return nlp_sentence

def _get_spans(nlp_sentence):
    spans = list(nlp_sentence.ents)
    spans_to_add = list()
    span_noun_chunks = list(nlp_sentence.noun_chunks)
    for span in span_noun_chunks:
        spans_to_add.append(span)

    spans = spans + spans_to_add
    return spans

def _filter_spans(spans):
    # Filter a sequence of spans so they don't contain overlaps
    get_sort_key = lambda span: (span.end - span.start, span.start)
    sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
    result = []
    seen_tokens = set()
    for span in sorted_spans:
        if span.start not in seen_tokens and span.end - 1 not in seen_tokens:
            result.append(span)
            seen_tokens.update(range(span.start, span.end))
    return result

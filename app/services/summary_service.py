from app.model_repository import nlp


def summarize(text):
    doc = nlp(text)
    tr = doc._.textrank

    sentences = tr.summary(limit_phrases=15, limit_sentences=3)
    summary = ' '.join([sent.text for sent in sentences])

    # TODO update summary in db

    return summary

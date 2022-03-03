from app.model_repository import nlp
from app.models import Request, Status
from app.database import db_session
from app.api.services.constants import PHRASE_LIMIT, SENTENCE_LIMIT


def create_summary(text):
    doc = nlp(text)
    tr = doc._.textrank

    sentences = tr.summary(limit_phrases=PHRASE_LIMIT, limit_sentences=SENTENCE_LIMIT)
    summary = ' '.join([sent.text for sent in sentences])

    return summary


def summarize(text, request_id):
    try:
        request = Request.query.filter_by(id=request_id).first()
        request.status = Status.RUNNING
        db_session.commit()

        summary = create_summary(text)

        request = Request.query.filter_by(id=request_id).first()
        request.summary = summary
        request.status = Status.FINISHED
        db_session.commit()

        return summary
    except Exception as ex:
        print(ex)
        request = Request.query.filter_by(id=request_id).first()
        request.status = Status.FAILED
        db_session.commit()

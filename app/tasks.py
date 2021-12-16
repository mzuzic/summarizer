import re
from . import celery

from app.database import db_session
from app.models import Request, Status
from app.services.storage_service import storage_service
from app.services.clauses.train import train as train_clauses
from app.services.document_status_service import update_training_information_finished, update_training_information_failed


@celery.task()
def train_clause_model(clauses, labels, request_id, trained_model_id):
    try:
        request = Request.query.filter_by(id=request_id).first()
        request.status = Status.RUNNING
        db_session.commit()

        model = train_clauses(clauses, labels)

        tempfile = storage_service.upload_ml_model(model)

        request.model_location = tempfile.file_path
        request.status = Status.FINISHED
        db_session.commit()

        update_training_information_finished(trained_model_id, tempfile.file_path)

    except Exception as ex:
        print(ex)
        request = Request.query.filter_by(id=request_id).first()
        request.status = Status.FAILED
        db_session.commit()

        update_training_information_failed(trained_model_id)



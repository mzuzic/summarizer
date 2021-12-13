from . import celery

from app.services.storage_service import storage_service
from app.services.clauses.train import train as train_clauses


@celery.task()
def train_clause_model(clauses, labels):
    model = train_clauses(clauses, labels)

    tempfile = storage_service.upload_ml_model(model)

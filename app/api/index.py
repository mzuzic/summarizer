from flask import (Blueprint, jsonify, request)

from app.database import init_db
from app.database import db_session
from app.db_models import Request

from app.services.fields.train import train as train_fields
from app.services.fields.predict import batch_predict_custom_fields
from app.services.storage_service import storage_service
from app.tasks import train_clause_model


index = Blueprint(name='index', import_name=__name__, url_prefix="/v1")
init_db()


@index.route('/custom-fields/train', methods=['POST'])
def train_custom_fields():
    trained_model_id = request.json.get('trained_model_id')
    model_name = request.json.get('model_name')
    examples = request.json.get('examples')
    contra_examples = request.json.get('contra_examples')  # counter examples taken from field database
    label = request.json.get('label')
    ent_type = request.json.get('ent_type')

    trained_knn = train_fields(examples, contra_examples, label, ent_type)
    _ = storage_service.upload_ml_model(model_name, trained_knn)

    return jsonify({"tempfile": "",
                    "name": model_name})


@index.route('/custom-fields/predict', methods=['POST'])
def predict_custom_fields():
    model_map = request.json.get('model_map')
    examples = request.json.get('examples')

    preds = batch_predict_custom_fields(examples, model_map)
    resp = {"results": preds}
    return jsonify(resp)


# CLAUSE ID ENDPOINTS
@index.route('/custom-clauses/train', methods=['POST'])
def train_custom_clauses():
    clauses = request.json.get('clauses')
    labels = request.json.get('labels')

    # name Task?
    req = Request()
    db_session.add(req)
    db_session.commit()

    train_clause_model.delay(clauses, labels, req.id)

    return jsonify({'request_id': req.id})

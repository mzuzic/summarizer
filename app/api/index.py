from flask import (Blueprint, Flask, jsonify, request)

from app.database import init_db
from app.database import db_session
from app.models import Request

from app.services.fields.train import train as train_fields
from app.services.fields.predict import batch_predict_custom_fields
from app.services.storage_service import storage_service
from app.tasks import train_clause_model


index = Blueprint(name='index', import_name=__name__, url_prefix="/v1")
init_db()

# FIELD ENDPOINT
@index.route('/custom-fields/train', methods=['POST'])
def train_custom_fields():
    examples = request.json.get('examples')
    label = request.json.get('label')
    ent_type = request.json.get('ent_type')

    trained_knn = train_fields(examples, label, ent_type)
    tempfile = storage_service.upload_ml_model(trained_knn)

    return jsonify({
                    "tempfile": tempfile.file_path,
                    "name": f'knn_{label}_{ent_type}'
                   })


@index.route('/custom-fields/predict', methods=['POST'])
def predict_custom_fields():
    model_map = request.json.get('model_map')
    examples = request.json.get('examples')
    
    preds = batch_predict_custom_fields(examples, model_map)
    resp = {"results": preds}
    return jsonify(resp)


@index.route('/batch-annotate', methods=['POST'])
def batch_annotate_api():
    # worker = WorkerService.getInstance()
    # worker.push_to_channel()
    clauses = request.json.get('clauses')
    results = batch_annotate(clauses)
    resp = {"results": results}
    return jsonify(resp)


# CLAUSE ENDPOINTS
@index.route('/custom-clauses/train', methods=['POST'])
def train_custom_clauses():
    clauses = request.json.get('clauses')
    labels = request.json.get('labels')
    trained_model_id = request.json.get('trained_model_id')

    req = Request()
    db_session.add(req)
    db_session.commit()

    train_clause_model.delay(clauses, labels, req.id, trained_model_id)

    return jsonify({'request_id': req.id})


# REQUEST ENDPOINT
@index.route('/request/<request_id>', methods=['GET'])
def get_request(request_id):
    request = Request.query.get(request_id)

    return jsonify(request)

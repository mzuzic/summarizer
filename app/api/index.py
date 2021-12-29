from flask import (Blueprint, jsonify, request)

from app.database import init_db
from app.database import db_session
from app.models import Request

from app.tasks import train_clause_model, train_fields_model


index = Blueprint(name='index', import_name=__name__, url_prefix="/v1")
init_db()

# FIELD ENDPOINT
@index.route('/custom-fields/train', methods=['POST'])
def train_custom_fields():
    trained_model_id = request.json.get('trained_model_id')
    model_name = request.json.get('model_name')
    examples = request.json.get('examples')
    contra_examples = request.json.get('contra_examples')  # counter examples taken from field database
    label = request.json.get('label')
    ent_type = request.json.get('ent_type')

    # name Task?
    req = Request()
    db_session.add(req)
    db_session.commit()

    train_fields_model.delay(trained_model_id, model_name, examples, contra_examples, label, ent_type, req.id)

    return jsonify({'request_id': req.id})


# CLAUSE ENDPOINTS
@index.route('/custom-clauses/train', methods=['POST'])
def train_custom_clauses():
    clauses = request.json.get('clauses')
    labels = request.json.get('labels')
    trained_model_id = request.json.get('trained_model_id')
    model_name = request.json.get('model_name')

    req = Request()
    db_session.add(req)
    db_session.commit()

    train_clause_model.delay(
        clauses,
        labels,
        req.id,
        trained_model_id,
        model_name
    )

    return jsonify({'request_id': req.id})


# REQUEST ENDPOINT
@index.route('/request/<request_id>', methods=['GET'])
def get_request(request_id):
    request = Request.query.get(request_id)

    return jsonify(request)

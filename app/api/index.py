from flask import (Blueprint, Flask, jsonify, request)

from app.services.fields.train import train as train_fields
from app.services.fields.predict import batch_predict_custom_fields
from app.services.storage_service import storage_service

index = Blueprint(name='index', import_name=__name__, url_prefix="/v1")


@index.route('/custom-fields/train', methods=['POST'])
def train_custom_fields():
    document_type_id = request.json.get('document_type_id')
    examples = request.json.get('examples')
    contra_examples = request.json.get('contra_examples') # counter examples taken from field database
    label = request.json.get('label')
    ent_type = request.json.get('ent_type')

    trained_knn = train_fields(examples, contra_examples, label, ent_type)
    model_name = f'fields_{document_type_id}_knn_{ent_type}_{cnt}'
    tempfile = storage_service.upload_ml_model(trained_knn)
    cnt = 1 # take from core-app the number of trained models

    return jsonify({
                    "tempfile": tempfile.file_path,
                    "name": model_name
                   })


@index.route('/custom-fields/predict', methods=['POST'])
def predict_custom_fields():
    model_map = request.json.get('model_map')
    examples = request.json.get('examples')
    
    preds = batch_predict_custom_fields(examples, model_map)
    resp = {"results": preds}
    return jsonify(resp)

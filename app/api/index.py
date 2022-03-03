import json

from flask import (Blueprint, jsonify, request)

from app.database import init_db, db_session
from app.models import Request
from app.services.summary_service import summarize


index = Blueprint(name='index', import_name=__name__, url_prefix="/v1")
init_db()


@index.route('/summary/<request_id>', methods=['GET'])
def get_summary(request_id):
    request = Request.query.get(request_id)

    return jsonify(request)


@index.route('/summarize', methods=['POST'])
def create_summary():
    transcript_file = request.files['transcript']
    content = json.load(transcript_file)
    transcript = content['results']['transcripts'][0]['transcript']

    # TODO create a repository?
    req = Request()
    db_session.add(req)
    db_session.commit()

    # TODO create as an async task
    summarize(transcript, req.id)

    return jsonify({'id': req.id})

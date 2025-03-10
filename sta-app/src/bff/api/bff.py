import bff.seedwork.presentation.api as api
import json
from bff.seedwork.domain.exceptions import DomainException
from flask import redirect, render_template, request, session, url_for
from flask import Response
import requests


bp = api.create_blueprint('bff', '/bff')


@bp.route('/ping', methods = ['GET'])
def ping() :
    return 'PONG', 200

@bp.route('/anonymized-data', methods=['GET'])
def anonymized_data():
    try:
        response = requests.get("http://34.132.113.112:5002/anonimizador/users")
        response.raise_for_status()
        data = response.json()
        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
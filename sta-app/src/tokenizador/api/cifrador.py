import saludtech.seedwork.presentation.api as api
import json
from saludtech.seedwork.domain.exceptions import DomainException
from flask import redirect, render_template, request, session, url_for
from flask import Response


bp = api.create_blueprint('cifrar', '/cifrar')

@bp.route('/carga', methods = ['POST'])
def carga() :
    login_data = request.json


@bp.route('/ping', methods = ['GET'])
def ping() :
    return 'PONG', 200
import bff.seedwork.presentation.api as api
import json
from bff.seedwork.domain.exceptions import DomainException
from flask import redirect, render_template, request, session, url_for
from flask import Response


bp = api.create_blueprint('bff', '/bff')

@bp.route('/login', methods = ['POST'])
def login() :
    login_data = request.json


@bp.route('/ping', methods = ['GET'])
def ping() :
    return 'PONG', 200

    
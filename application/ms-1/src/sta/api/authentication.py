import sta.seedwork.presentation.api as api

from flask import request
from sta.authentication.application.mappers import AuthenticationMapperDTOJson

bp = api.create_blueprint('authentication', '/authentication')

@bp.route("/login", methods = ('GET',))
def login_async() :
    mapper = AuthenticationMapperDTOJson()

    return mapper.external_to_dto(request.json)
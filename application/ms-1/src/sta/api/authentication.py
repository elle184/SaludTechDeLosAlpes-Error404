import sta.seedwork.presentation.api as api

bp = api.create_blueprint('authentication', '/authentication')

@bp.route("/login", methods = ('GET',))
def home() :
    return 'Hello, World!'
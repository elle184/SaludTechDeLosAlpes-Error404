import os

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_swagger import swagger

# Identifica el directorio base
basedir = os.path.abspath(os.path.dirname(__file__))

def importar_modelos_alchemy():
    ...
    '''import aeroalpes.modulos.cliente.infraestructura.dto
    import aeroalpes.modulos.hoteles.infraestructura.dto
    import aeroalpes.modulos.pagos.infraestructura.dto
    import aeroalpes.modulos.precios_dinamicos.infraestructura.dto
    import aeroalpes.modulos.vehiculos.infraestructura.dto
    import aeroalpes.modulos.vuelos.infraestructura.dto'''

def create_app(configuracion=None):
    # Init la aplicacion de Flask
    app = Flask(__name__, instance_relative_config=True)

    if configuracion is not None and configuracion["TESTING"]:
        app.config['SQLALCHEMY_DATABASE_URI'] =\
            'sqlite:///' + configuracion["DATABASE"]
    
    # Configuracion de BD
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] =\
            'sqlite:///' + os.path.join(basedir, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

     # Inicializa la DB
    #from aeroalpes.config.db import init_db
    #init_db(app)

    #from aeroalpes.config.db import db

    importar_modelos_alchemy()

    with app.app_context():
        ...
        #db.create_all()

     # Importa Blueprints
    from . import clients

    # Registro de Blueprints
    app.register_blueprint(clients.bp)

    @app.route("/spec")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "Api BFF"
        return jsonify(swag)

    return app
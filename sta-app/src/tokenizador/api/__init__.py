import os

from flask import Flask, jsonify, redirect, render_template, request, url_for
from flask_swagger import swagger
import logging
import pulsar
from ..modules.tokenizador.infraestructure.consumer import suscribirse_a_eventos
import threading


logging.basicConfig(level=logging.DEBUG) 

logging.info("iniciando tokenizador.")  # Añade logs

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
            'sqlite:///' + os.path.join(basedir, 'databasetoken.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    thread1 = threading.Thread(target=suscribirse_a_eventos, name="Thread-anonimizacion")
    thread1.start()

     # Inicializa la DB
    #from aeroalpes.config.db import init_db
    #init_db(app)

    #from aeroalpes.config.db import db

    importar_modelos_alchemy()

    with app.app_context():
        ...
        #db.create_all()

     # Importa Blueprints
    from . import tokenizador

    # Registro de Blueprints
    app.register_blueprint(tokenizador.bp)

    @app.route('/health')
    def health():
        return "OK", 200 

    @app.route("/specToken")
    def spec():
        swag = swagger(app)
        swag['info']['version'] = "1.0"
        swag['info']['title'] = "Api SaludTech"
        return jsonify(swag)

    return app

app = create_app()
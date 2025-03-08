import anonimizador.seedwork.presentation.api as api
import json
from anonimizador.seedwork.domain.exceptions import DomainException
from flask import  request, jsonify, current_app


bp = api.create_blueprint('anonimizador', '/anonimizador')


data = []  # Inicializa data aquí

@bp.before_app_first_request
def load_data_once():
    load_data()


@bp.route('/ping', methods = ['GET'])
def ping() :
    return 'PONG', 200


def load_data(filename="/src/anonimizador/api/data.json"):
    current_app.logger.info('LLamando data')
    current_app.logger.info('Archivo un : %s', str(filename))
    global data
    try:
        with open(filename, "r") as f:
            current_app.logger.info('bien corre bien')
            data = json.load(f)
            current_app.logger.info('info archivo : %s', str(data))
    except FileNotFoundError:
        current_app.logger.info('no carga')
        data = []  # Si el archivo no existe, se inicializa la lista vacía
# Rutas de la API

@bp.route('/users', methods=['GET'])
def get_users():
    current_app.logger.info('Entra al get')
    return jsonify(data)

@bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    for user in data:
        if user["User"]["id"] == user_id:  # Asumiendo que tienes un campo "id" en tu JSON
            return jsonify(user)
    return jsonify({"message": "Usuario no encontrado"}), 404

@bp.route('/users', methods=['POST'])
def create_user():
    new_user = request.get_json()
    # Asignar un ID único al nuevo usuario (puedes usar un contador o UUID)
    new_user["User"]["id"] = len(data) + 1  # Ejemplo simple con contador
    data.append(new_user)
    return jsonify(new_user), 201

@bp.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    updated_user = request.get_json()
    for i, user in enumerate(data):
        if user["User"]["id"] == user_id:
            data[i] = updated_user
            return jsonify(updated_user)
    return jsonify({"message": "Usuario no encontrado"}), 404

@bp.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    for i, user in enumerate(data):
        if user["User"]["id"] == user_id:
            del data[i]
            return jsonify({"message": "Usuario eliminado"})
    return jsonify({"message": "Usuario no encontrado"}), 404

    
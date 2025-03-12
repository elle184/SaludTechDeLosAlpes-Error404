import bff.seedwork.presentation.api as api
import json
from bff.seedwork.domain.exceptions import DomainException
from flask import redirect, render_template, request, session, url_for, jsonify
from flask import Response
import requests
import random

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

@bp.route('/process-data', methods=['POST'])
def process_data():
    try:
        payload = request.get_json()
        print(payload)
        token = request.headers.get('Authorization')
        if not token or not token.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid Authorization header"}), 401
        token = token.split(' ')[1]

        response = requests.post(
            "http://35.208.102.128/saga",
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}"
            },
            json=payload
        )

        # Check if request was successful
        response.raise_for_status()

        # Check if response has content before parsing JSON
        if response.text.strip():
            try:
                data = response.json()
                print(data)  # Print after successful parsing
                return jsonify(data), 200
            except json.JSONDecodeError as json_err:
                print(f"Invalid JSON response: {response.text}")
                return jsonify({"error": "Invalid response format from server"}), 500
        else:
            # Handle empty response
            print("Empty response received")
            return jsonify({"message": "Request processed successfully but no data returned"}), 200

    except requests.exceptions.RequestException as e:
        print(f"Request error: {str(e)}")
        return jsonify({"error": str(e)}), 500

@bp.route('/auth', methods=['GET'])
def auth():
    try:
        user_id = random.randint(1, 4)
        response = requests.get(
            f"http://35.209.10.96:5001/tokenizador/users/{user_id}",
        )
        response.raise_for_status()
        data = response.json()
        return jsonify(data), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"error": str(e)}), 500
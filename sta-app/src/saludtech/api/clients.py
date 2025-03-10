import saludtech.seedwork.presentation.api as api
import json
from saludtech.seedwork.domain.exceptions import DomainException
from flask import redirect, render_template, request, session, url_for
from flask import Response


bp = api.create_blueprint('clientes', '/clientes')

@bp.route('/login', methods = ['POST'])
def login() :
    login_data = request.json


@bp.route('/ping', methods = ['GET'])
def ping() :
    return 'PONG', 200


@bp.route('/processed-data', methods=['GET'])
def processed_data():
    import random
    from datetime import datetime, timedelta

    # Generate random health data
    data = {
        "patients": []
    }

    # Generate random patient records
    for i in range(random.randint(3, 7)):
        gender = random.choice(['Male', 'Female'])
        age = random.randint(18, 85)

        # Vital signs
        heart_rate = random.randint(60, 100)
        systolic = random.randint(100, 140)
        diastolic = random.randint(60, 90)
        temperature = round(random.uniform(36.1, 37.5), 1)

        # Common medical conditions
        conditions = ["Hypertension", "Diabetes Type 2", "Asthma", "Arthritis", "Obesity"]
        patient_conditions = random.sample(conditions, random.randint(0, 2))

        # Visit date
        days_ago = random.randint(1, 60)
        last_visit = (datetime.now() - timedelta(days=days_ago)).strftime("%Y-%m-%d")

        patient = {
            "patient_id": f"P{random.randint(10000, 99999)}",
            "age": age,
            "gender": gender,
            "vital_signs": {
                "heart_rate": heart_rate,
                "blood_pressure": f"{systolic}/{diastolic}",
                "temperature": temperature
            },
            "lab_results": {
                "glucose": random.randint(70, 140),
                "cholesterol": random.randint(150, 240)
            },
            "medical_conditions": patient_conditions,
            "last_visit": last_visit
        }

        data["patients"].append(patient)

    data["total_patients"] = len(data["patients"])
    data["generated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return data
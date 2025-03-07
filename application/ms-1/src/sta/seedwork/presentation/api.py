from flask import Blueprint

def create_blueprint(identificator : str, prefix : str) :
    return Blueprint(identificator, __name__, url_prefix = prefix)
import os
from flask import Flask

basedir = os.path.abspath(os.path.dirname(__file__))

def create_app() :
    app = Flask(__name__)

    from . import authentication

    app.register_blueprint(authentication.bp)

    return app

if __name__ == "__main__" :
    app.run(host = '0.0.0.0', port = 8000, debug = True)
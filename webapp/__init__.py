from flask import Flask
from .transaction.connection_manager import close_connection
from .init_app import init_app

import webapp.authentication.sign_up as sign_up
import webapp.authentication.login as login
import os

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping({
        "SECRET_KEY": "dev",
        "DATABASE": {
            "user": "root",
            "password": "rOOt",
            "database": "burger_builder",
            "host": "localhost",
            "port": 3306
        }
    })

    if test_config:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError: 
        pass
    
    init_app(app)

    app.register_blueprint(sign_up.bp)
    app.register_blueprint(login.bp)

    return app

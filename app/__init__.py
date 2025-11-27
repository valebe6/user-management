from flask import Flask
from app.config import Config
from flasgger import Swagger
from app.db import mongo
from app.errors import register_error_handlers
from app.users.routes import users_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    mongo.init_app(app)
    app.register_blueprint(users_bp, url_prefix="/api/users")
    
    swagger_config = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
    "openapi": "3.0.2",
    }

    swagger_template = {
        "info": {
            "title": "Users API",
            "description": "CRUD básico de usuarios con Flask + MongoDB",
            "version": "1.0.0",
        }
    }

    Swagger(app, config=swagger_config, template=swagger_template)
    
    register_error_handlers(app)

    return app

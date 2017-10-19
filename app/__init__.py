# app/__init__.py
import json
from flask_api import FlaskAPI, status
from flask_sqlalchemy import SQLAlchemy
from flask import request, jsonify, abort, make_response

from instance.config import app_config

# initialize db
db = SQLAlchemy()


def create_app(config_name):

    from app.models import Program

    app = FlaskAPI(__name__, instance_relative_config=True)
    app.config.from_object(app_config[config_name])
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)


    # import the organization blueprint and register it on the app
    from .organization import org_blueprint
    from .programs import program_blueprint
    from .services import service_blueprint
    from .locations import location_blueprint

    app.register_blueprint(org_blueprint)
    app.register_blueprint(program_blueprint)
    app.register_blueprint(service_blueprint)
    app.register_blueprint(location_blueprint)

    return app

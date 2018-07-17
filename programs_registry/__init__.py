# -*- coding: utf-8 -*-

import os
from flask import Flask
from flask_migrate import Migrate

from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__) 
    app.config.from_object(app_config.get(config_name))

    # IMPORTANT: initialize SQLAlchemy before Marshmallow
    from .api.models import db
    db.init_app(app)

    from .api.schemas import ma
    ma.init_app(app)

    # IMPORTANT: initialize Flask-Migrate extension
    migrate = Migrate(app, db)

    from .api.router import api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api')

    return app


# for 'flask run'
app = create_app(config_name=os.environ.get('FLASK_ENV'))

if __name__ == '__main__':
    app.run()
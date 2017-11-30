import os
import connexion

from instance.config import app_config
from flask_sqlalchemy import SQLAlchemy

# initialize db
db = SQLAlchemy()

config_name = os.getenv('APP_SETTINGS')
app = connexion.App(__name__)
app.add_api('openapi.yaml')

flask_app = app.app
flask_app.instance_relative_config = True
flask_app.config.from_object(app_config[config_name])
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(flask_app)

# import the blueprints and register it on the app
from app.organization import org_blueprint
from app.programs import program_blueprint
from app.services import service_blueprint
from app.locations import location_blueprint
from app.physical_address import address_blueprint

flask_app.register_blueprint(org_blueprint)
flask_app.register_blueprint(program_blueprint)
flask_app.register_blueprint(service_blueprint)
flask_app.register_blueprint(location_blueprint)
flask_app.register_blueprint(address_blueprint)

if __name__ == "__main__":
    flask_app.run(port=8080)

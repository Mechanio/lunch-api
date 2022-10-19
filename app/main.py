from flask import Flask
from flask_jwt_extended import JWTManager
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

from config import Config
from .database.database import db, base


def setup_database(app):
    with app.app_context():
        @app.before_first_request
        def create_tables():
            base.metadata.create_all(db)


def setup_jwt(app):
    jwt = JWTManager(app)

    from app.models import RevokedTokenModel

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        jti = jwt_payload['jti']
        return RevokedTokenModel.is_jti_blacklisted(jti)


def setup_swagger(app):
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yaml'
    swagger_bp = get_swaggerui_blueprint(SWAGGER_URL, API_URL, config={'app_name': "Lunch API"})
    app.register_blueprint(swagger_bp, url_prefix=SWAGGER_URL)


def create_app():
    app = Flask(__name__)
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config.from_object(Config)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    setup_database(app)
    setup_jwt(app)
    setup_swagger(app)

    from .views import restaurants_bp, choices_bp, employees_bp, menus_bp, auth_bp
    app.register_blueprint(restaurants_bp)
    app.register_blueprint(choices_bp)
    app.register_blueprint(employees_bp)
    app.register_blueprint(menus_bp)
    app.register_blueprint(auth_bp)

    return app

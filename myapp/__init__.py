from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import (
JWTManager, jwt_required, create_access_token, create_refresh_token,
get_jwt_identity, unset_jwt_cookies
)
import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    from .configs import getURI
    from .controller import routeApi
    app.config['SQLALCHEMY_DATABASE_URI'] = getURI()
    app.config['SQLALCHEMY_ECHO'] = True
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['JWT_SECRET_KEY'] = Config.key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = Config.access
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = Config.refresh

    jwt = JWTManager(app)

    db.init_app(app)
    migrate.init_app(app, db)
    from .entity import User, Photo
    # db.create_all()

    routeApi(app)

    return app
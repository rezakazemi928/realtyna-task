from os import getenv

from api.helpers import (
    IdIsNotValid,
    InvalidRequestArgs,
    ReservationNotFound,
    UserNotFound,
    handle_error_response,
)
from api.routes.blueprint import blueprint
from configs import Development, Production
from extensions import db, ma, migrate
from flask import Flask, current_app
from marshmallow import ValidationError
from sqlalchemy import exc


def create_app():
    app = Flask(__name__)
    app_env = getenv("FLASK_ENV", "production")
    config = {
        "production": Production,
        "development": Development,
    }
    app.config.from_object(config[app_env])

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app=app, db=db)
    app.register_blueprint(blueprint)

    @app.errorhandler(ValidationError)
    def handle_marshmallow_error(e):
        """
        Return json error for marshmallow validation errors.

        This will avoid having to try/catch ValidationErrors in all endpoints, returning
        correct JSON response with associated HTTP 400 Status (https://tools.ietf.org/html/rfc7231#section-6.5.1)
        """
        return handle_error_response(
            type="SchemaValidationError",
            code=11,
            sub_code=10,
            status=400,
            msg=e.message,
            mimetype="application/json",
        )

    @app.errorhandler(exc.SQLAlchemyError)
    def handle_sqlalchemy_error(e):
        """
        Return json error for sqlalchemy error.

        This will avoid having to try/catch SQLalchemyError in all endpoints, returning
        correct JSON response with associated HTTP 500 status.
        """
        current_app.logger.error(e._message)
        db.session.rollback()
        return handle_error_response(
            type="DatabaseError",
            code=12,
            sub_code=100,
            status=500,
            mimetype="application/json",
            msg=e._message,
        )

    @app.errorhandler(IdIsNotValid)
    def handle_invalid_id(e):
        return handle_error_response(
            type="RequestError",
            code=13,
            sub_code=100,
            status=400,
            mimetype="application/json",
        )

    @app.errorhandler(UserNotFound)
    def handle_not_found_user(e):
        return handle_error_response(
            type="RequestError",
            code=13,
            sub_code=101,
            status=404,
            mimetype="application/json",
        )

    @app.errorhandler(InvalidRequestArgs)
    def handle_invalid_req_args(e):
        return handle_error_response(
            type="RequestArgsError",
            code=14,
            sub_code=100,
            status=400,
            mimetype="application/json",
        )

    @app.errorhandler(ReservationNotFound)
    def handle_invalid_not_found_option(e):
        return handle_error_response(
            type="RequestError",
            code=13,
            sub_code=102,
            status=400,
            mimetype="application/json",
        )

    return app

from flask import Flask
from os import getenv

from extensions import db, ma, migrate
from configs import Development, Production
from api.routes.blueprint import blueprint


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
    
    return app
from datetime import timedelta
from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Base:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_BLACKLIST_ENABLED = True
    JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=10)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=20)


class Development(Base):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}"
        f"@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
    )
    JWT_SECRET_KEY = "h8Cx+xDIlAxiZrziP5PL/w=="


class Production(Base):
    pass

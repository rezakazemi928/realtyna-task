from os import getenv

from dotenv import load_dotenv

load_dotenv()


class Base:
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class Development(Base):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}"
        f"@{getenv('POSTGRES_HOST')}:{getenv('POSTGRES_PORT')}/{getenv('POSTGRES_DB')}"
    )

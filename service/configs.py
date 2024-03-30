from os import getenv

from dotenv import load_dotenv

load_dotenv()

print()


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


class TestConfig(Base):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = (
        f"postgresql://{getenv('POSTGRES_USER', 'root')}:{getenv('POSTGRES_PASSWORD', '6o0fHIUW/9BApROyKXBmLg===')}"
        f"@{getenv('POSTGRES_HOST', '127.0.0.1')}:{getenv('POSTGRES_PORT', '5433')}/{getenv('POSTGRES_DB', 'postgres')}"
    )

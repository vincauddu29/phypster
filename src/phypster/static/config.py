class Config(object):
    pass

class ProdConfig(Config):
    DEBUG = False
    SECRET_KEY = ""
    SQLALCHEMY_DATABASE_URI = ""
    JWT_SECRET_KEY = ""


class DevConfig(Config):
    DEBUG = True
    SECRET_KEY = "change_me_secret_key"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://myapp:myapp@localhost:5432/myapp"
    SQLALCHEMY_ECHO = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "change_me_jwt"

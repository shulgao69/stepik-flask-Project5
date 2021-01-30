# class Config:
#     DEBUG = True
#     SECRET_KEY= "randomstring"
#     SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@127.0.0.1:5432/data7"
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     PASSWORD_MIN_LENGTH = 8


import os

db_path = os.environ.get('DATABASE_URL')
secret_key = os.environ.get("SECRET_KEY")
# flaskapp = os.environ.get("FLASK_APP")


class Config:
    DEBUG = True
    # FLASK_APP=flaskapp
    SECRET_KEY= secret_key
    SQLALCHEMY_DATABASE_URI = db_path
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PASSWORD_MIN_LENGTH = 8
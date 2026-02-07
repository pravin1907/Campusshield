import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = 'your-secret-key'  # change to a random secret
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'campus.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')

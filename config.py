import os


class Config:
    SECRET_KEY = 'admin-secret-key-123'

    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:password@localhost/enterprise_db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
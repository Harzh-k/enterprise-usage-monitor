from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#Create the database object
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    #Load configuration from config.py
    app.config.from_object('config.Config')

    #Initialize the database with the app
    db.init_app(app)

    #Import and register the routes
    from .routes import main
    app.register_blueprint(main)

    #Create the tables in MySQL if they don't exist
    with app.app_context():
        db.create_all()

    return app
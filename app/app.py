from flask import Flask
from flask_pymongo import PyMongo
from db import close_db

def create_app():
    app = Flask(__name__)

    # Load configuration
    app.config.from_object('config.Config')

    # Initialize Flask-PyMongo
    mongo = PyMongo(app)

    # Register the webhook route
    from webhook import webhook as webhook_blueprint
    app.register_blueprint(webhook_blueprint)

    app.teardown_appcontext(close_db)

    return app

